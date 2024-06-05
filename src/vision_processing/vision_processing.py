from typing import TypedDict
import numpy as np
import cv2


def masking_first_step(img_data, lower_hsv, upper_hsv):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(img_data, cv2.COLOR_RGB2HSV)

    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    return mask


def clean_mask_second_step(mask_data):
    # Threshold the mask if necessary (this will ensure binary mask)
    _, binary_mask = cv2.threshold(mask_data, 127, 255, cv2.THRESH_BINARY)

    # Define a kernel for morphological operations
    kernel = np.ones((5, 5), np.uint8)

    # Apply morphological operations
    # Erosion followed by dilation (Opening) to remove small outliers
    cleaned_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, kernel)

    # Apply closing to close small holes
    cleaned_mask = cv2.morphologyEx(cleaned_mask, cv2.MORPH_CLOSE, kernel)
    return cleaned_mask


def remove_unconnected_components_third_step(cleaned_mask_data):
    # Threshold the mask if necessary (this will ensure binary mask)
    _, binary_mask = cv2.threshold(cleaned_mask_data, 127, 255, cv2.THRESH_BINARY)

    # Perform connected components analysis
    _, labels, stats, _ = cv2.connectedComponentsWithStats(binary_mask, connectivity=8)

    if len(stats) <= 1:
        return cleaned_mask_data

    # Find the component with the largest area, skip the background
    largest_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])

    # Create an empty mask to draw the largest component
    largest_component_mask = np.zeros_like(binary_mask)
    largest_component_mask[labels == largest_label] = 255
    return largest_component_mask


def get_mask_frame_fourth_step(final_mask):
    """Calculates a bounding box around the target with a small margin"""
    # Threshold the mask if necessary (this will ensure a binary mask)
    _, binary_mask = cv2.threshold(final_mask, 127, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(
        binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if len(contours) == 0:  # No target found
        return False, ((0, 0), (0, 0)), (0, 0)

    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Get the bounding rectangle of the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Calculate the center coordinates of the bounding box
    x_center = x + w // 2
    y_center = y + h // 2

    # Calculate the increase in size (1% of the image's height)
    increase = int(0.01 * final_mask.shape[0])

    # Calculate the new bounding rectangle
    x_new = max(0, x - increase)
    y_new = max(0, y - increase)
    w_new = min(final_mask.shape[1] - x_new, w + 2 * increase)
    h_new = min(final_mask.shape[0] - y_new, h + 2 * increase)

    return True, ((x_new, y_new), (x_new + w_new, y_new + h_new)), (x_center, y_center)


def get_object_distance_and_is_within_threshold_fifth_step(
    full_image, target_xy_1: tuple[int, int], target_xy_2: tuple[int, int], magic_number
):
    # if object frame width is 70% or more of image width, don't continue
    percentage_threshold = 70

    width = full_image.shape[1]
    x1, _ = target_xy_1
    x2, _ = target_xy_2
    frame_width = x2 - x1

    frame_width_percentage = (frame_width / width) * 100
    distance = magic_number / frame_width_percentage
    return (
        distance,
        frame_width_percentage,
        (frame_width_percentage < percentage_threshold),
    )


def get_lateral_position_offset_sixth_step(target_center_xy, frame):
    width = frame.shape[1]
    x = target_center_xy[0]
    min_x, max_x = (-1, 1)
    lateral_pos_offset = x * (max_x - min_x) / width + min_x
    return lateral_pos_offset


def get_contour_from_mask_seventh_step(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)

    num_vertices = 999
    epsilon = 1  # initial epsilon value is n + 1
    while num_vertices > 6:
        epsilon += 1
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)
        num_vertices = len(approx)
    return num_vertices, approx


def get_facing_from_contour_eighth_step(contour_vertices):
    """Either FRONT, LEFT or RIGHT, derived from target shape"""

    def angle_with_x_axis(vector):
        """Calculate the angle between a vector and the x-axis."""
        angle_rad = np.arctan2(-vector[0][1], vector[0][0])
        angle_deg = np.degrees(angle_rad)

        if angle_deg < 0:
            angle_deg += 180
        return angle_deg

    def side_length(start_vertex, end_vertex):
        """Calculate the length of a side given two vertices."""
        return np.linalg.norm(end_vertex - start_vertex)

    def facing_from_short_angle_pair(a1, a2):
        """Calculate object facing given angle of short sides."""
        deg_threshold = 7
        if abs(a1 - 90) < deg_threshold or abs(a2 - 90) < deg_threshold:
            return "FRONT"
        if a1 > 90 and a2 > 90:
            return "RIGHT"
        return "LEFT"

    contour_parallel_indeces = [(0, 3), (1, 4), (2, 5)]
    contour_parallel_angles = []
    shortest_parallel_side_l = 999999
    shortest_parallel_side_index = 0
    for index, (i, j) in enumerate(contour_parallel_indeces):
        start_vertex_i = contour_vertices[i]
        end_vertex_i = contour_vertices[(i + 1) % len(contour_vertices)]
        direction_vector_i = end_vertex_i - start_vertex_i
        l_i = side_length(start_vertex_i, end_vertex_i)
        start_vertex_j = contour_vertices[j]
        end_vertex_j = contour_vertices[(j + 1) % len(contour_vertices)]
        direction_vector_j = end_vertex_j - start_vertex_j
        l_j = side_length(
            start_vertex_j,
            end_vertex_j,
        )
        if l_i + l_j < shortest_parallel_side_l:
            shortest_parallel_side_index = index
            shortest_parallel_side_l = l_i + l_j
        contour_parallel_angles.append(
            (
                angle_with_x_axis(direction_vector_i),
                angle_with_x_axis(direction_vector_j),
            )
        )

    a1, a2 = contour_parallel_angles[shortest_parallel_side_index]
    return facing_from_short_angle_pair(a1, a2)


def get_rotation_from_contour_facing_ninth_step(contour_vertices, facing):
    """Rotation angle (deg) goes from 0 to (45, -45)"""

    def side_length(start_vertex, end_vertex):
        """Calculate the length of a side given two vertices."""
        return np.linalg.norm(end_vertex - start_vertex)

    def furthest_x_vertex_pairs(vertices):
        """Get the pairs of vertices furthest from center on the x-axis"""
        vertices_list = [tuple(pair[0]) for pair in vertices]
        sorted_vertices = sorted(vertices_list, key=lambda vertex: vertex[0])

        most_left = np.array([sorted_vertices[0], sorted_vertices[1]])
        most_right = np.array([sorted_vertices[-2], sorted_vertices[-1]])
        return (most_left, most_right)

    def normalized_width_from_x_vertex_extremes(most_left, most_right):
        all_vertices = [most_left[0], most_left[1], most_right[0], most_right[1]]
        sorted_vertices = sorted(
            all_vertices, key=lambda vertex: vertex[1], reverse=True
        )
        highest_y_vertices = sorted_vertices[:2]
        norm_width = abs(highest_y_vertices[0][0] - highest_y_vertices[1][0])
        return norm_width

    def rotation_from_norm_width_height(norm_width, height):
        x = max(norm_width / height, 1)  # 1 < val < sqrt(2)
        map_min, map_max = 0, 45  # map val (1, sqrt(2)) to (0, 45)
        return (x - 1) * (map_max - map_min) / (np.sqrt(2) - 1) + map_min

    def normalized_rotation_from_rot_facing(rotation, facing):
        if facing == "LEFT":
            return -rotation
        return rotation

    if facing == "FRONT":
        return 0
    most_left, most_right = furthest_x_vertex_pairs(contour_vertices)
    norm_width = normalized_width_from_x_vertex_extremes(most_left, most_right)
    height = side_length(most_left[0], most_left[1])
    rot = rotation_from_norm_width_height(norm_width, height)
    final_rot = normalized_rotation_from_rot_facing(rot, facing)
    return final_rot


def write_debug_frame(frame, outline_positions, data_text_lines):
    debug_frame = frame.copy()
    xy_1, xy_2 = outline_positions
    cv2.rectangle(debug_frame, xy_1, xy_2, color=(0, 230, 0), thickness=2)
    for i, line in enumerate(data_text_lines):
        cv2.putText(
            debug_frame,
            line,
            (10, 26 + i * 32),
            cv2.FONT_HERSHEY_DUPLEX,
            0.8,
            (0, 255, 255),
            2,
            2,
        )
    cv2.imwrite("debug.jpg", cv2.cvtColor(debug_frame, cv2.COLOR_BGR2RGB))


class TargetAnalysisResult(TypedDict):
    target_detected: bool
    """True if target was detected, otherwise False, and analysis values can be ignored."""

    target_size_percentage: float
    """Percentage of frame pixels that the target occupies"""

    target_too_close: bool
    """Target is too close to observer for accurate analysis values, so they can be ignored."""

    target_distance: float
    """Target distance from observer, measured in cm."""

    target_frame_lateral_position_offset: float
    """How far from frame center the target is, between `-1` and `1`. `0` represents the center
    of the frame, `-1` is the left-most position, and `1` is the right-most position."""

    target_rotation: float
    """Target rotation in frame with respect to the observer, in degrees, between `-45` and `45`.
    If the target is perfectly facing the observer, this value is `0`. If it is facing right,
    the value is `-45`, left is `45`, and anything in between."""


LOWER_RED_HSV = np.array([0, 100, 100])
UPPER_RED_HSV = np.array([200, 255, 255])
TARGET_DIST_MAGIC_NUMBER = 640


def analyze_frame_for_target_object(frame, debug=False) -> TargetAnalysisResult:
    """Analyzes an image frame for a target object and calculates its parameters"""
    mask = masking_first_step(frame, LOWER_RED_HSV, UPPER_RED_HSV)
    clean_mask = clean_mask_second_step(mask)
    final_mask = remove_unconnected_components_third_step(clean_mask)
    found_frame, target_frame, frame_center_xy = get_mask_frame_fourth_step(final_mask)
    if not found_frame:
        if debug:
            write_debug_frame(frame, target_frame, ["Looking for target"])
        return {
            "target_detected": False,
            "target_size_percentage": 0,
            "target_too_close": False,
            "target_frame_lateral_position_offset": 0,
            "target_rotation": 0,
            "target_distance": 0,
        }
    target_xy_1, target_xy_2 = target_frame
    target_distance, target_size_percentage, is_in_distance_threshold = (
        get_object_distance_and_is_within_threshold_fifth_step(
            frame, target_xy_1, target_xy_2, TARGET_DIST_MAGIC_NUMBER
        )
    )
    if not is_in_distance_threshold:
        if debug:
            write_debug_frame(frame, target_frame, ["Target too close"])
        return {
            "target_detected": True,
            "target_size_percentage": target_size_percentage,
            "target_too_close": True,
            "target_frame_lateral_position_offset": 0,
            "target_rotation": 0,
            "target_distance": 0,
        }
    target_lateral_offset = get_lateral_position_offset_sixth_step(
        frame_center_xy, frame
    )
    num_vertices, target_contour = get_contour_from_mask_seventh_step(final_mask)
    if num_vertices != 6:
        if debug:
            write_debug_frame(
                frame,
                target_frame,
                [
                    "Target shape unrecognized",
                    f"Distance: {target_distance:.2f}cm",
                    f"Center offset: {target_lateral_offset:.2f}",
                ],
            )
        return {
            "target_detected": True,
            "target_size_percentage": target_size_percentage,
            "target_too_close": True,
            "target_frame_lateral_position_offset": target_lateral_offset,
            "target_rotation": 0,
            "target_distance": target_distance,
        }
    target_facing = get_facing_from_contour_eighth_step(target_contour)
    target_rotation = get_rotation_from_contour_facing_ninth_step(
        target_contour, target_facing
    )
    if debug:
        write_debug_frame(
            frame,
            target_frame,
            [
                f"Distance: {target_distance:.2f}cm",
                f"Rotation: {target_rotation:.2f}deg",
                f"Center offset: {target_lateral_offset:.2f}",
            ],
        )
    return {
        "target_detected": True,
        "target_size_percentage": target_size_percentage,
        "target_too_close": False,
        "target_frame_lateral_position_offset": target_lateral_offset,
        "target_rotation": target_rotation,
        "target_distance": target_distance,
    }


class DestinationAnalysisResult(TypedDict):
    destination_detected: bool
    """True if destination was detected, otherwise False, and analysis values can be ignored."""

    destination_distance: float
    """Destination distance from observer, measured in cm."""

    destination_frame_lateral_position_offset: float
    """How far from frame center the destination is, between `-1` and `1`. `0` represents the center
    of the frame, `-1` is the left-most position, and `1` is the right-most position."""


LOWER_YELLOW_HSV = np.array([10, 100, 100])
UPPER_YELLOW_HSV = np.array([45, 255, 255])
DESTINATION_DIST_MAGIC_NUMBER = 580


def analyze_frame_for_destination(frame, debug=False) -> DestinationAnalysisResult:
    """Analyzes an image frame for a destination position and calculates its parameters"""
    mask = masking_first_step(frame, LOWER_YELLOW_HSV, UPPER_YELLOW_HSV)
    clean_mask = clean_mask_second_step(mask)
    final_mask = remove_unconnected_components_third_step(clean_mask)
    found_frame, destination_frame, frame_center_xy = get_mask_frame_fourth_step(
        final_mask
    )
    if not found_frame:
        if debug:
            write_debug_frame(frame, destination_frame, ["Looking for destination"])
        return {
            "destination_detected": False,
            "destination_distance": 0,
            "destination_frame_lateral_position_offset": 0,
        }
    destination_xy_1, destination_xy_2 = destination_frame
    destination_distance, _, _ = get_object_distance_and_is_within_threshold_fifth_step(
        frame, destination_xy_1, destination_xy_2, DESTINATION_DIST_MAGIC_NUMBER
    )
    destionation_lateral_offset = get_lateral_position_offset_sixth_step(
        frame_center_xy, frame
    )
    if debug:
        write_debug_frame(
            frame,
            destination_frame,
            [
                f"Destination distance: {destination_distance:.2f}cm",
                f"Center offset: {destionation_lateral_offset:.2f}",
            ],
        )
    return {
        "destination_detected": True,
        "destination_distance": destination_distance,
        "destination_frame_lateral_position_offset": destionation_lateral_offset,
    }

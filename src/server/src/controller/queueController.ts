import { FastifyInstance } from 'fastify';
import { Static, Type } from '@sinclair/typebox';
import { StateService } from '../service/stateService';

export default async function queueController(fastify: FastifyInstance) {
  const stateService = new StateService();

  const MessageTypes = Type.Union([
    Type.Literal('CALIB_DATA_TARGET'),
    Type.Literal('CALIB_DATA_DESTINATION'),
    Type.Literal('START_MACHINE'),
    Type.Literal('STOP_MACHINE'),
  ]);

  const CalibrationData = Type.Object({
    upper: Type.String(),
    lower: Type.String(),
  });

  const PostQueueMessage = Type.Object({
    type: MessageTypes,
    data: CalibrationData,
  });

  type PostQueueMessageType = Static<typeof PostQueueMessage>;

  const PostQueueMessageReply = Type.Object({
    success: Type.Boolean(),
    message: Type.String(),
  });

  type PostQueueMessageReplyType = Static<typeof PostQueueMessageReply>;

  // Add message posted from external source to incoming queue
  fastify.post<{ Body: PostQueueMessageType; Reply: PostQueueMessageReplyType }>(
    '/incoming',
    {
      schema: {
        body: PostQueueMessage,
        response: {
          200: PostQueueMessageReply,
        },
      },
    },
    async (request, reply) => {
      const message = request.body;
      stateService.processMachineMessage(message);
      reply.send({ success: true, message: 'Message added to queue' });
    },
  );

  const GetQueueMessageReply = Type.Object({
    type: Type.Union([
      Type.Literal('CALIBRATE_TARGET'),
      Type.Literal('CALIBRATE_DESTINATION'),
      Type.Literal('START_MACHINE'),
      Type.Literal('STOP_MACHINE'),
    ]),
    data: Type.Union([Type.Null(), Type.Number()]),
  });

  type GetQueueMessageReplyType = Static<typeof GetQueueMessageReply>;

  // Retrieve message posted from internal source to outgoing queue
  fastify.get<{ Reply: GetQueueMessageReplyType }>('/outgoing', async (_request, reply) => {
    const message = stateService.readMachineFIFO();
    if (message === undefined) {
      reply.code(204);
      return;
    }

    reply.send({ ...message, data: null });
  });
}

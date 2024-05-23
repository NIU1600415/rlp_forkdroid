import axios from "axios";

const instance = axios.create({
  baseURL: "http://localhost:3006",
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
  },
  responseType: "json",
});

const log = async (url: string, body?: object) => {
  console.log(`[API] ${url} ${body ? JSON.stringify(body) : ""}`);
};

const Api = {
  get: <T>(url: string) =>
    log(url).then(() =>
      instance.get(url).then((response) => response.data as T)
    ),
  post: <T>(url: string, body: object) =>
    log(url, body).then(() =>
      instance.post(url, body).then((response) => response.data as T)
    ),
  patch: (url: string, body?: object) =>
    log(url, body).then(() =>
      instance.patch(url, body).then((response) => response.data)
    ),
  put: (url: string, body: object) =>
    log(url, body).then(() =>
      instance.put(url, body).then((response) => response.data)
    ),
  delete: (url: string) =>
    log(url).then(() => instance.delete(url).then((response) => response.data)),
};

export default Api;

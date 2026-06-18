import http from "node:http";
import { addAttachment, getTask } from "./task-store.js";

function sendJson(response, statusCode, payload) {
  response.writeHead(statusCode, { "Content-Type": "application/json; charset=utf-8" });
  response.end(JSON.stringify(payload, null, 2));
}

function readJsonBody(request) {
  return new Promise((resolve, reject) => {
    let body = "";
    request.on("data", (chunk) => {
      body += chunk;
    });
    request.on("end", () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (error) {
        reject(error);
      }
    });
    request.on("error", reject);
  });
}

const server = http.createServer(async (request, response) => {
  const url = new URL(request.url, "http://localhost:3000");
  const pathParts = url.pathname.split("/").filter(Boolean);

  if (request.method === "GET" && pathParts[0] === "tasks" && pathParts.length === 2) {
    const task = getTask(pathParts[1]);
    if (!task) {
      sendJson(response, 404, { message: "任务不存在" });
      return;
    }
    sendJson(response, 200, task);
    return;
  }

  if (
    request.method === "POST" &&
    pathParts[0] === "tasks" &&
    pathParts[2] === "attachments"
  ) {
    try {
      const body = await readJsonBody(request);
      const result = addAttachment(pathParts[1], body);
      sendJson(response, result.status, result.ok ? result.task : { message: result.message });
    } catch {
      sendJson(response, 400, { message: "请求体必须是合法 JSON" });
    }
    return;
  }

  sendJson(response, 404, { message: "未找到对应接口" });
});

server.listen(3000, () => {
  console.log("minimal-task-board listening on http://localhost:3000");
});

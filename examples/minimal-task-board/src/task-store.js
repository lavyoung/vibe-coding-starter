const tasks = new Map([
  [
    "task-1",
    {
      id: "task-1",
      title: "整理 starter 文档",
      attachments: []
    }
  ]
]);

const MAX_ATTACHMENTS = 3;

export function getTask(taskId) {
  return tasks.get(taskId) ?? null;
}

export function addAttachment(taskId, attachment) {
  const task = getTask(taskId);
  if (!task) {
    return { ok: false, status: 404, message: "任务不存在" };
  }

  if (!attachment.filename || !attachment.url) {
    return { ok: false, status: 400, message: "filename 和 url 都不能为空" };
  }

  if (task.attachments.length >= MAX_ATTACHMENTS) {
    return { ok: false, status: 400, message: "每个任务最多上传 3 个附件" };
  }

  const saved = {
    id: `att-${task.attachments.length + 1}`,
    filename: attachment.filename,
    url: attachment.url
  };
  task.attachments.push(saved);
  return { ok: true, status: 201, task };
}

package com.example.devicecenter.model;

import jakarta.validation.constraints.NotBlank;

/**
 * 创建设备请求。
 *
 * @param name 设备名称
 * @author OpenAI
 * @since 2026/06/18
 */
public record CreateDeviceRequest(
        @NotBlank(message = "name must not be blank")
        String name
) {
}

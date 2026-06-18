package com.example.devicecenter.model;

import jakarta.validation.constraints.NotBlank;

/**
 * 设备图片上传请求。
 *
 * @param imageUrl 图片 URL
 * @author OpenAI
 * @since 2026/06/18
 */
public record UploadDeviceImageRequest(
        @NotBlank(message = "imageUrl must not be blank")
        String imageUrl
) {
}

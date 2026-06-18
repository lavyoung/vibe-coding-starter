package com.example.devicecenter.model;

import java.util.List;

/**
 * 设备响应对象。
 *
 * @param id 设备 ID
 * @param name 设备名称
 * @param imageUrls 图片地址列表
 * @author OpenAI
 * @since 2026/06/18
 */
public record DeviceResponse(
        Long id,
        String name,
        List<String> imageUrls
) {
}

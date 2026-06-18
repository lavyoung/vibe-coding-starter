package com.example.devicecenter.controller;

import com.example.devicecenter.model.CreateDeviceRequest;
import com.example.devicecenter.model.DeviceResponse;
import com.example.devicecenter.model.UploadDeviceImageRequest;
import com.example.devicecenter.service.DeviceService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 设备管理示例接口，演示 controller 层如何受 docs-first 文档驱动。
 *
 * @author OpenAI
 * @since 2026/06/18
 */
@RestController
@RequestMapping("/admin/devices")
public class DeviceAdminController {

    private final DeviceService deviceService;

    public DeviceAdminController(DeviceService deviceService) {
        this.deviceService = deviceService;
    }

    /**
     * 创建设备。
     *
     * @param request 创建请求
     * @return 设备详情
     */
    @PostMapping
    public DeviceResponse createDevice(@Valid @RequestBody CreateDeviceRequest request) {
        return deviceService.createDevice(request);
    }

    /**
     * 查询设备详情。
     *
     * @param deviceId 设备 ID
     * @return 设备详情
     */
    @GetMapping("/{deviceId}")
    public DeviceResponse getDevice(@PathVariable Long deviceId) {
        return deviceService.getDevice(deviceId);
    }

    /**
     * 上传设备图片 URL。
     *
     * @param deviceId 设备 ID
     * @param request 图片上传请求
     * @return 更新后的设备详情
     */
    @PostMapping("/{deviceId}/images")
    public DeviceResponse uploadImage(
            @PathVariable Long deviceId,
            @Valid @RequestBody UploadDeviceImageRequest request
    ) {
        return deviceService.uploadImage(deviceId, request);
    }
}

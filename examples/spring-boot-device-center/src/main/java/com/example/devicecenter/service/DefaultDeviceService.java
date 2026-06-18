package com.example.devicecenter.service;

import com.example.devicecenter.model.CreateDeviceRequest;
import com.example.devicecenter.model.Device;
import com.example.devicecenter.model.DeviceResponse;
import com.example.devicecenter.model.UploadDeviceImageRequest;
import com.example.devicecenter.repository.DeviceRepository;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;

/**
 * 设备服务实现，演示受设计文档约束的业务规则落地。
 *
 * <p>当前规则：</p>
 * <p>1. 创建设备时仅需要名称</p>
 * <p>2. 每台设备最多保留 3 张图片 URL</p>
 *
 * @author OpenAI
 * @since 2026/06/18
 */
@Service
public class DefaultDeviceService implements DeviceService {

    private static final int MAX_IMAGE_COUNT = 3;

    private final DeviceRepository deviceRepository;

    public DefaultDeviceService(DeviceRepository deviceRepository) {
        this.deviceRepository = deviceRepository;
    }

    /**
     * 创建设备。
     *
     * @param request 创建设备请求
     * @return 新建设备详情
     */
    @Override
    public DeviceResponse createDevice(CreateDeviceRequest request) {
        Long deviceId = deviceRepository.nextId();
        Device device = new Device(deviceId, request.name(), List.of());
        return toResponse(deviceRepository.save(device));
    }

    /**
     * 查询设备。
     *
     * @param deviceId 设备 ID
     * @return 设备详情
     */
    @Override
    public DeviceResponse getDevice(Long deviceId) {
        return toResponse(getRequiredDevice(deviceId));
    }

    /**
     * 给设备追加图片 URL。
     *
     * @param deviceId 设备 ID
     * @param request 图片上传请求
     * @return 更新后的设备详情
     */
    @Override
    public DeviceResponse uploadImage(Long deviceId, UploadDeviceImageRequest request) {
        Device device = getRequiredDevice(deviceId);
        if (device.getImageUrls().size() >= MAX_IMAGE_COUNT) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "device image count exceeds limit");
        }
        device.addImageUrl(request.imageUrl());
        return toResponse(deviceRepository.save(device));
    }

    private Device getRequiredDevice(Long deviceId) {
        return deviceRepository.findById(deviceId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "device not found"));
    }

    private DeviceResponse toResponse(Device device) {
        return new DeviceResponse(device.getId(), device.getName(), device.getImageUrls());
    }
}

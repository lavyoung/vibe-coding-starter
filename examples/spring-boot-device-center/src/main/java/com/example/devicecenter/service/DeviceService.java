package com.example.devicecenter.service;

import com.example.devicecenter.model.CreateDeviceRequest;
import com.example.devicecenter.model.DeviceResponse;
import com.example.devicecenter.model.UploadDeviceImageRequest;

/**
 * 设备服务接口。
 *
 * @author OpenAI
 * @since 2026/06/18
 */
public interface DeviceService {

    DeviceResponse createDevice(CreateDeviceRequest request);

    DeviceResponse getDevice(Long deviceId);

    DeviceResponse uploadImage(Long deviceId, UploadDeviceImageRequest request);
}

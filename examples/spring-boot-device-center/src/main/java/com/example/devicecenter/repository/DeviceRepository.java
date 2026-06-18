package com.example.devicecenter.repository;

import com.example.devicecenter.model.Device;

import java.util.Optional;

/**
 * 设备仓储接口，演示企业项目中常见的 repository 抽象层。
 *
 * @author OpenAI
 * @since 2026/06/18
 */
public interface DeviceRepository {

    Long nextId();

    Device save(Device device);

    Optional<Device> findById(Long deviceId);
}

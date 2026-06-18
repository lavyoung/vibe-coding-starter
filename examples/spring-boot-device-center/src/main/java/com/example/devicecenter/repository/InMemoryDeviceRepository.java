package com.example.devicecenter.repository;

import com.example.devicecenter.model.Device;
import org.springframework.stereotype.Repository;

import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

/**
 * 内存仓储实现，用于保持示例可运行，同时保留 repository 分层结构。
 *
 * @author OpenAI
 * @since 2026/06/18
 */
@Repository
public class InMemoryDeviceRepository implements DeviceRepository {

    private final AtomicLong idGenerator = new AtomicLong(0);
    private final Map<Long, Device> devices = new ConcurrentHashMap<>();

    @Override
    public Long nextId() {
        return idGenerator.incrementAndGet();
    }

    @Override
    public Device save(Device device) {
        devices.put(device.getId(), device);
        return device;
    }

    @Override
    public Optional<Device> findById(Long deviceId) {
        return Optional.ofNullable(devices.get(deviceId));
    }
}

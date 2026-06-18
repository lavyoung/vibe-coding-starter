package com.example.devicecenter.model;

import java.util.ArrayList;
import java.util.List;

/**
 * 示例领域对象，表示设备及其图片 URL 列表。
 *
 * @author OpenAI
 * @since 2026/06/18
 */
public class Device {

    private final Long id;
    private final String name;
    private final List<String> imageUrls;

    public Device(Long id, String name, List<String> imageUrls) {
        this.id = id;
        this.name = name;
        this.imageUrls = new ArrayList<>(imageUrls);
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public List<String> getImageUrls() {
        return new ArrayList<>(imageUrls);
    }

    public void addImageUrl(String imageUrl) {
        imageUrls.add(imageUrl);
    }
}

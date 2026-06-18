package com.example.devicecenter.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * 控制器测试，验证示例项目的最小接口闭环。
 *
 * @author OpenAI
 * @since 2026/06/18
 */
@SpringBootTest
@AutoConfigureMockMvc
class DeviceAdminControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void shouldCreateAndQueryDevice() throws Exception {
        Long deviceId = createDevice("Front Desk Printer");

        mockMvc.perform(get("/admin/devices/" + deviceId))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(deviceId))
                .andExpect(jsonPath("$.name").value("Front Desk Printer"))
                .andExpect(jsonPath("$.imageUrls").isArray());
    }

    @Test
    void shouldRejectFourthImageUpload() throws Exception {
        Long deviceId = createDevice("Counter Printer");

        for (int index = 1; index <= 3; index++) {
            mockMvc.perform(post("/admin/devices/" + deviceId + "/images")
                            .contentType(MediaType.APPLICATION_JSON)
                            .content(objectMapper.writeValueAsString(
                                    new UploadDeviceImageBody("https://cdn.example.com/device-" + index + ".png")
                            )))
                    .andExpect(status().isOk())
                    .andExpect(jsonPath("$.imageUrls.length()").value(index));
        }

        mockMvc.perform(post("/admin/devices/" + deviceId + "/images")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(
                                new UploadDeviceImageBody("https://cdn.example.com/device-4.png")
                        )))
                .andExpect(status().isConflict());
    }

    private Long createDevice(String name) throws Exception {
        MvcResult result = mockMvc.perform(post("/admin/devices")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(new CreateDeviceBody(name))))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value(name))
                .andReturn();

        return objectMapper.readTree(result.getResponse().getContentAsString()).get("id").asLong();
    }

    private record CreateDeviceBody(String name) {
    }

    private record UploadDeviceImageBody(String imageUrl) {
    }
}

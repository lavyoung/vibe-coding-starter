package com.example.devicecenter.controller;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping;
import org.yaml.snakeyaml.Yaml;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * OpenAPI 契约一致性测试：把运行时路由（RequestMappingHandlerMapping）与
 * 契约文档 docs/api/v1.2.0/device-admin-api.yaml 双向对比，防止"契约与实现"漂移。
 *
 * <p>这是 docs-first 体系中"内容对齐"唯一能机器化的部分：契约已登记但代码没有的
 * 端点、代码已实现但契约未登记的端点都会让本测试失败。修改接口时，代码与契约必须
 * 同步改动，否则本测试在 CI（check_all 的 mvn test）中直接拦截。
 *
 * @author OpenAI
 * @since 2026/08/17
 */
@SpringBootTest
class OpenApiContractConsistencyTest {

    /** 契约文件相对 Maven 模块根目录（surefire 的工作目录） */
    private static final Path CONTRACT_FILE = Path.of("docs/api/v1.2.0/device-admin-api.yaml");

    private static final Set<String> OPERATION_METHODS =
            Set.of("get", "put", "post", "delete", "patch", "options", "head", "trace");

    @Autowired
    private RequestMappingHandlerMapping handlerMapping;

    @Test
    void contractAndRuntimeRoutesMustMatch() throws Exception {
        Set<String> contractRoutes = routesFromContract(loadContract());
        Set<String> runtimeRoutes = routesFromRuntime();

        Set<String> onlyInContract = new HashSet<>(contractRoutes);
        onlyInContract.removeAll(runtimeRoutes);
        Set<String> onlyInRuntime = new HashSet<>(runtimeRoutes);
        onlyInRuntime.removeAll(contractRoutes);

        StringBuilder message = new StringBuilder();
        if (!onlyInContract.isEmpty()) {
            message.append("契约已登记但运行时不存在：").append(sorted(onlyInContract))
                    .append(System.lineSeparator());
        }
        if (!onlyInRuntime.isEmpty()) {
            message.append("运行时存在但契约未登记：").append(sorted(onlyInRuntime))
                    .append(System.lineSeparator());
        }
        assertTrue(message.isEmpty(), message.toString());
    }

    private Map<String, Object> loadContract() throws Exception {
        assertTrue(Files.exists(CONTRACT_FILE),
                "契约文件不存在：" + CONTRACT_FILE.toAbsolutePath());
        return new Yaml().load(Files.readString(CONTRACT_FILE));
    }

    private Set<String> routesFromContract(Map<String, Object> contract) {
        Set<String> routes = new HashSet<>();
        @SuppressWarnings("unchecked")
        Map<String, Object> paths = (Map<String, Object>) contract.get("paths");
        for (Map.Entry<String, Object> entry : paths.entrySet()) {
            for (String method : OPERATION_METHODS) {
                if (((Map<?, ?>) entry.getValue()).containsKey(method)) {
                    routes.add(method.toUpperCase() + " " + entry.getKey());
                }
            }
        }
        return routes;
    }

    private Set<String> routesFromRuntime() {
        Set<String> routes = new HashSet<>();
        handlerMapping.getHandlerMethods().forEach((info, method) -> {
            Set<String> patterns = info.getPathPatternsCondition() == null
                    ? Set.of()
                    : info.getPathPatternsCondition().getPatternValues();
            Set<RequestMethod> methods = info.getMethodsCondition().getMethods();
            for (String pattern : patterns) {
                if (pattern.equals("/error")) {
                    continue; // Spring Boot 默认错误端点不属于业务契约
                }
                if (methods.isEmpty()) {
                    continue; // 未限定 HTTP 方法的映射不参与契约对比
                }
                for (RequestMethod requestMethod : methods) {
                    routes.add(requestMethod.name() + " " + pattern);
                }
            }
        });
        return routes;
    }

    private static String sorted(Set<String> values) {
        return values.stream().sorted().toList().toString();
    }
}

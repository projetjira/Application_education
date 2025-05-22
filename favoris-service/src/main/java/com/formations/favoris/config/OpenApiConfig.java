package com.formations.favoris.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.License;
import io.swagger.v3.oas.models.servers.Server;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.ArrayList;
import java.util.List;

/**
 * Configuration for OpenAPI 3.0 documentation (Swagger UI)
 */
@Configuration
public class OpenApiConfig {

    @Value("${server.port}")
    private int serverPort;

    @Bean
    public OpenAPI favorisOpenAPI() {
        // Define servers
        List<Server> servers = new ArrayList<>();
        
        // Add server on current port
        servers.add(new Server()
                .url("http://localhost:" + serverPort)
                .description("Server on port " + serverPort));
        
        // Also add port 9090 as common port for favoris service
        if (serverPort != 9090) {
            servers.add(new Server()
                    .url("http://localhost:9090")
                    .description("Default development server"));
        }

        return new OpenAPI()
                .servers(servers)
                .info(new Info()
                        .title("API de gestion des favoris")
                        .description("API pour gérer les favoris des utilisateurs dans l'application éducative")
                        .version("1.0.0")
                        .contact(new Contact()
                                .name("Équipe de développement")
                                .email("contact@formations.com"))
                        .license(new License()
                                .name("Apache 2.0")
                                .url("https://www.apache.org/licenses/LICENSE-2.0")));
    }
}
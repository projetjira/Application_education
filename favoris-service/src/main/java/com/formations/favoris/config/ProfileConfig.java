package com.formations.favoris.config;

import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.event.ContextRefreshedEvent;
import org.springframework.context.event.EventListener;
import org.springframework.core.env.Environment;

import java.util.Arrays;

/**
 * Configuration to ensure proper profile activation
 */
@Configuration
@Slf4j
public class ProfileConfig {

    private final Environment environment;

    public ProfileConfig(Environment environment) {
        this.environment = environment;
    }

    @EventListener
    public void handleContextRefresh(ContextRefreshedEvent event) {
        log.info("Active profiles: {}", Arrays.toString(environment.getActiveProfiles()));
        
        // Log database connection info but hide sensitive information
        String mongoUri = environment.getProperty("spring.data.mongodb.uri");
        if (mongoUri != null) {
            // Extract just the server part to avoid logging credentials
            String maskedUri = mongoUri.replaceAll("mongodb\\+srv://[^@]+@", "mongodb+srv://***:***@");
            log.info("Using MongoDB connection: {}", maskedUri);
        } else {
            log.warn("MongoDB URI is not configured!");
        }
    }
}

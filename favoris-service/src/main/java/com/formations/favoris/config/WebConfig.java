package com.formations.favoris.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
import org.springframework.web.filter.CorsFilter;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * Web configuration for handling CORS and other web-related settings
 */
@Configuration
@EnableWebMvc
public class WebConfig implements WebMvcConfigurer {

    @Bean
    public CorsFilter corsFilter() {
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        CorsConfiguration config = new CorsConfiguration();
        
        // Allow all origins for development, but you should restrict this in production
        config.setAllowCredentials(true);
        config.addAllowedOrigin("http://localhost:3000"); // Student frontend
        config.addAllowedOrigin("http://localhost:3001"); // Admin frontend if on a different port
        config.addAllowedOrigin("http://localhost:4200"); // Angular frontend if using that
        config.addAllowedOrigin("http://localhost:8000"); // Backend service
        config.addAllowedOrigin("http://localhost:8001"); // Books service
        
    
        
        // Allow common HTTP methods
        config.addAllowedMethod("GET");
        config.addAllowedMethod("POST");
        config.addAllowedMethod("PUT");
        config.addAllowedMethod("DELETE");
        config.addAllowedMethod("OPTIONS");
        
        // Allow all headers
        config.addAllowedHeader("*");
        
        // Set max age to 1 hour (3600 seconds)
        config.setMaxAge(3600L);
        
        source.registerCorsConfiguration("/api/**", config);
        return new CorsFilter(source);
    }
}

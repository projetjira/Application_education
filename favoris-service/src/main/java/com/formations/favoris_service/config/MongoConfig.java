package com.formations.favoris_service.config;

import com.mongodb.ConnectionString;
import com.mongodb.MongoClientSettings;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.config.AbstractMongoClientConfiguration;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Collection;
import java.util.Collections;

/**
 * MongoDB configuration with compatibility settings for MongoDB Atlas
 */
@Configuration
@EnableMongoRepositories(basePackages = "com.formations.favoris_service.repository")
public class MongoConfig extends AbstractMongoClientConfiguration {

    private static final Logger log = LoggerFactory.getLogger(MongoConfig.class);

    @Value("${spring.data.mongodb.uri}")
    private String mongoUri;

    @Value("${spring.data.mongodb.database:favoris_db}")
    private String databaseName;

    static {
        // Setting necessary SSL properties for MongoDB Atlas connectivity
        System.setProperty("jdk.tls.client.protocols", "TLSv1.2");
        System.setProperty("com.mongodb.sslInvalidHostNameAllowed", "true");
    }

    @Override
    protected String getDatabaseName() {
        return databaseName;
    }

    @Override
    public MongoClient mongoClient() {
        log.info("Initializing MongoDB client with Atlas compatibility settings");
        try {
            // Use the pure connection string - all settings handled in the URI
            MongoClientSettings settings = MongoClientSettings.builder()
                .applyConnectionString(new ConnectionString(mongoUri))
                .applyToSslSettings(builder -> 
                    builder.enabled(true)
                           .invalidHostNameAllowed(true)
                )
                .build();
            
            return MongoClients.create(settings);
        } catch (Exception e) {
            log.error("Failed to create MongoDB client: {}", e.getMessage(), e);
            throw new RuntimeException("MongoDB connection failed", e);
        }
    }

    @Override
    protected Collection<String> getMappingBasePackages() {
        return Collections.singleton("com.formations.favoris_service.model");
    }

    @Bean
    public MongoTemplate mongoTemplate() throws Exception {
        return new MongoTemplate(mongoClient(), getDatabaseName());
    }
}

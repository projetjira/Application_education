package com.formations.favoris.config;

import com.mongodb.ConnectionString;
import com.mongodb.MongoClientSettings;
import com.mongodb.MongoCredential;
import com.mongodb.ServerApi;
import com.mongodb.ServerApiVersion;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.connection.ConnectionPoolSettings;
import com.mongodb.connection.SocketSettings;
import com.mongodb.connection.SslSettings;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.data.mongodb.config.AbstractMongoClientConfiguration;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Collection;
import java.util.Collections;
import java.util.concurrent.TimeUnit;

/**
 * Configuration MongoDB améliorée avec gestion de la resilience pour MongoDB Atlas
 */
@Configuration
@EnableMongoRepositories(basePackages = "com.formations.favoris.repository")
@Profile("!dev")
public class MongoConfig extends AbstractMongoClientConfiguration {

    private static final Logger log = LoggerFactory.getLogger(MongoConfig.class);

    @Value("${spring.data.mongodb.uri}")
    private String mongoUri;

    @Value("${spring.data.mongodb.database:favoris_db}")
    private String databaseName;

    @Value("${spring.data.mongodb.connection-timeout:30000}")
    private int connectionTimeout;

    @Value("${spring.data.mongodb.socket-timeout:60000}")
    private int socketTimeout;

    static {
        // Résolution des problèmes SSL avec MongoDB Atlas
        System.setProperty("jdk.tls.client.protocols", "TLSv1.2");
        // Additional SSL fixes for MongoDB Atlas
        System.setProperty("jsse.enableSNIExtension", "false");
    }

    @Override
    public String getDatabaseName() {
        return databaseName;
    }
    
    @Override
    public MongoClient mongoClient() {
        log.info("Initializing MongoDB client with connection settings");
        try {
            ConnectionString connectionString = new ConnectionString(mongoUri);
            
            log.debug("Configuring MongoDB client settings with timeout values: connection={}, socket={}", 
                connectionTimeout, socketTimeout);
            
            MongoClientSettings mongoClientSettings = MongoClientSettings.builder()
                .applyConnectionString(connectionString)
                // Using a simplified ServerApi configuration
                .serverApi(ServerApi.builder()
                    .version(ServerApiVersion.V1)
                    .strict(false)  // Disable strict mode for better compatibility
                    .deprecationErrors(false)
                    .build())
                // Configure SSL settings with error handling
                .applyToSslSettings(sslBuilder -> {
                    sslBuilder.enabled(true)
                              .invalidHostNameAllowed(true);
                    log.debug("SSL settings configured with invalidHostNameAllowed=true");
                })
                // Increase connection pool settings for better reliability
                .applyToConnectionPoolSettings(builder -> 
                    builder.maxConnectionIdleTime(120000, TimeUnit.MILLISECONDS)
                           .maxConnectionLifeTime(300000, TimeUnit.MILLISECONDS)
                           .maxSize(20)
                           .minSize(5)
                           .maxWaitTime(60000, TimeUnit.MILLISECONDS)
                )
                // Increase socket timeouts with user-defined values
                .applyToSocketSettings(builder -> 
                    builder.connectTimeout(connectionTimeout, TimeUnit.MILLISECONDS)
                           .readTimeout(socketTimeout, TimeUnit.MILLISECONDS)
                )
                // Enable retries for better resilience
                .retryWrites(true)
                .retryReads(true)
                .build();
            
            log.info("MongoDB client settings successfully configured");
            return MongoClients.create(mongoClientSettings);
        } catch (Exception e) {
            log.error("Failed to create MongoDB client", e);
            // Rethrow as runtime exception to fail fast during application startup
            throw new RuntimeException("Could not initialize MongoDB connection", e);
        }
    }

    @Override
    protected Collection<String> getMappingBasePackages() {
        return Collections.singleton("com.formations.favoris.model");
    }

    @Bean
    public MongoTemplate mongoTemplate() {
        return new MongoTemplate(mongoClient(), getDatabaseName());
    }
}

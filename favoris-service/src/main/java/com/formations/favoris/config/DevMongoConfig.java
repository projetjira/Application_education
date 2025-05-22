package com.formations.favoris.config;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.data.mongodb.config.AbstractMongoClientConfiguration;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

import java.util.Collection;
import java.util.Collections;

/**
 * Configuration MongoDB pour le développement local
 * Utilise une base de données MongoDB embarquée
 */
@Configuration
@EnableMongoRepositories(basePackages = "com.formations.favoris.repository")
@Profile("dev")
public class DevMongoConfig extends AbstractMongoClientConfiguration {

    private static final String DATABASE_NAME = "favoris_db";
    
    @Override
    protected String getDatabaseName() {
        return DATABASE_NAME;
    }
    
    @Override
    protected Collection<String> getMappingBasePackages() {
        return Collections.singleton("com.formations.favoris.model");
    }

    @Bean
    @Override
    public MongoClient mongoClient() {
        return MongoClients.create("mongodb://localhost:27017");
    }
    
    @Bean
    public MongoTemplate mongoTemplate() {
        return new MongoTemplate(mongoClient(), getDatabaseName());
    }
}

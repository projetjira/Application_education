package com.formations.favoris.config;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.autoconfigure.condition.ConditionalOnBean;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.core.MongoTemplate;

@Configuration
@ConditionalOnProperty(name = "spring.data.mongodb.uri")
public class MongoDbHealthCheck {

    @Bean
    @ConditionalOnBean(MongoTemplate.class)
    public CommandLineRunner checkMongoDbConnection(MongoTemplate mongoTemplate) {
        return args -> {
            try {
                // Tente d'accéder à la base de données
                System.out.println("Vérification de la connexion MongoDB...");
                System.out.println("Nom de la base de données: " + mongoTemplate.getDb().getName());
                System.out.println("Connexion MongoDB établie avec succès!");
            } catch (Exception e) {
                System.err.println("Erreur de connexion à MongoDB: " + e.getMessage());
                e.printStackTrace();
            }
        };
    }
}
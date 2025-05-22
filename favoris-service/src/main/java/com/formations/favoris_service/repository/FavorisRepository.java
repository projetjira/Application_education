package com.formations.favoris_service.repository;

import com.formations.favoris_service.model.Favoris;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface FavorisRepository extends MongoRepository<Favoris, String> {
    List<Favoris> findByUserId(String userId);
    
    @Query("{'userId': ?0, 'formationId': ?1}")
    Optional<Favoris> findByUserIdAndFormationId(String userId, String formationId);
    
    List<Favoris> findByUserIdAndActifTrue(String userId);
    
    void deleteByUserIdAndFormationId(String userId, String formationId);
} 
package com.formations.favoris_service.service;

import com.formations.favoris_service.model.Favoris;
import com.formations.favoris_service.repository.FavorisRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
public class FavorisService {

    @Autowired
    private FavorisRepository favorisRepository;

    @Cacheable(value = "favoris", key = "#userId")
    public List<Favoris> getFavorisByUserId(String userId) {
        return favorisRepository.findByUserIdAndActifTrue(userId);
    }

    @CacheEvict(value = "favoris", key = "#favoris.userId")
    public Favoris addFavoris(Favoris favoris) {
        Optional<Favoris> existingFavoris = favorisRepository.findByUserIdAndFormationId(
            favoris.getUserId(), 
            favoris.getFormationId()
        );

        if (existingFavoris.isPresent()) {
            Favoris existing = existingFavoris.get();
            existing.setActif(true);
            existing.setDateAjout(LocalDateTime.now());
            return favorisRepository.save(existing);
        }

        favoris.setDateAjout(LocalDateTime.now());
        favoris.setActif(true);
        return favorisRepository.save(favoris);
    }

    @CacheEvict(value = "favoris", key = "#userId")
    public void removeFavoris(String userId, String formationId) {
        favorisRepository.deleteByUserIdAndFormationId(userId, formationId);
    }

    @CacheEvict(value = "favoris", key = "#userId")
    public void toggleFavoris(String userId, String formationId) {
        Optional<Favoris> existingFavoris = favorisRepository.findByUserIdAndFormationId(userId, formationId);
        
        if (existingFavoris.isPresent()) {
            Favoris favoris = existingFavoris.get();
            favoris.setActif(!favoris.isActif());
            favoris.setDateAjout(LocalDateTime.now());
            favorisRepository.save(favoris);
        } else {
            Favoris newFavoris = new Favoris();
            newFavoris.setUserId(userId);
            newFavoris.setFormationId(formationId);
            newFavoris.setActif(true);
            newFavoris.setDateAjout(LocalDateTime.now());
            favorisRepository.save(newFavoris);
        }
    }

    public boolean isFavoris(String userId, String formationId) {
        return favorisRepository.findByUserIdAndFormationId(userId, formationId)
            .map(Favoris::isActif)
            .orElse(false);
    }
} 
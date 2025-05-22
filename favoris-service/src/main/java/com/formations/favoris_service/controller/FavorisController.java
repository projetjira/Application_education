package com.formations.favoris_service.controller;

import com.formations.favoris_service.model.Favoris;
import com.formations.favoris_service.service.FavorisService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/favoris")
@Tag(name = "Favoris Controller", description = "APIs pour gérer les favoris des utilisateurs")
@CrossOrigin(origins = "*")
public class FavorisController {

    @Autowired
    private FavorisService favorisService;

    @GetMapping("/user/{userId}")
    @Operation(summary = "Récupérer tous les favoris d'un utilisateur")
    public ResponseEntity<List<Favoris>> getFavorisByUserId(@PathVariable String userId) {
        return ResponseEntity.ok(favorisService.getFavorisByUserId(userId));
    }

    @PostMapping
    @Operation(summary = "Ajouter un favori")
    public ResponseEntity<Favoris> addFavoris(@RequestBody Favoris favoris) {
        return ResponseEntity.ok(favorisService.addFavoris(favoris));
    }

    @DeleteMapping("/{userId}/{formationId}")
    @Operation(summary = "Supprimer un favori")
    public ResponseEntity<Void> removeFavoris(
            @PathVariable String userId,
            @PathVariable String formationId) {
        favorisService.removeFavoris(userId, formationId);
        return ResponseEntity.ok().build();
    }

    @PutMapping("/toggle/{userId}/{formationId}")
    @Operation(summary = "Basculer l'état d'un favori")
    public ResponseEntity<Void> toggleFavoris(
            @PathVariable String userId,
            @PathVariable String formationId) {
        favorisService.toggleFavoris(userId, formationId);
        return ResponseEntity.ok().build();
    }

    @GetMapping("/check/{userId}/{formationId}")
    @Operation(summary = "Vérifier si une formation est en favori")
    public ResponseEntity<Boolean> isFavoris(
            @PathVariable String userId,
            @PathVariable String formationId) {
        return ResponseEntity.ok(favorisService.isFavoris(userId, formationId));
    }
} 
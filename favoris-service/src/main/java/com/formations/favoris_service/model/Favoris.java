package com.formations.favoris_service.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import java.io.Serializable;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "favoris")
@CompoundIndex(def = "{'userId': 1, 'formationId': 1}", unique = true)
public class Favoris implements Serializable {
    @Id
    private String id;
    private String userId;
    private String formationId;
    private LocalDateTime dateAjout;
    private boolean actif;
} 
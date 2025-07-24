package com.example.hackathon.controller;

import com.example.hackathon.model.Scenario;
import com.example.hackathon.repository.ScenarioRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/game")
@CrossOrigin(origins = "http://localhost:3000")
public class GameController {
    private final ScenarioRepository repo;
    public GameController(ScenarioRepository repo) { this.repo = repo; }

    @GetMapping("/scenarios")
    public List<Scenario> getAll() {
        return repo.findAll();
    }
}

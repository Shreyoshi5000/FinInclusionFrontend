package com.example.hackathon.controller;

import com.example.hackathon.model.User;
//import com.example.hackathon.security.JwtUtil;
import com.example.hackathon.service.UserService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/auth")
@CrossOrigin(origins = "*")
public class AuthController {
    @Autowired
    private UserService userService;

    @GetMapping
    public ResponseEntity<String> test_api(){
        return ResponseEntity.ok("API is reachable");
    }

    @PostMapping("/signup")
    public ResponseEntity<?> signup(@RequestBody Map<String, String> request) {
        String username = request.get("username");
        String password = request.get("password");
        String role = request.get("role");
        if (username == null || password == null || role == null)
            return ResponseEntity.badRequest().body(Map.of("message", "Missing fields"));
        if (userService.usernameExists(username))
            return ResponseEntity.badRequest().body(Map.of("message", "Username already exists"));
        userService.registerUser(username, password, role);
        return ResponseEntity.ok(Map.of("message", "Signup successful"));
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody Map<String, String> request) {
        String username = request.get("username");
        String password = request.get("password");
        if (username == null || password == null)
            return ResponseEntity.badRequest().body(Map.of("message", "Missing fields"));

        Optional<User> userOpt = userService.authenticate(username, password);
        if (userOpt.isEmpty())
            return ResponseEntity.status(401).body(Map.of("message", "Invalid username or password"));

        User user = userOpt.get();
        return ResponseEntity.ok(Map.of("role", user.getRole()));
    }
}
package com.example.hackathon.service;

import com.example.hackathon.model.User;
import com.example.hackathon.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import java.util.Optional;

@Service
public class UserService {
    @Autowired
    private UserRepository userRepository;

    private final BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();

    public boolean usernameExists(String username) {
        return userRepository.findByUsername(username).isPresent();
    }

    public User registerUser(String username, String rawPassword, String role) {
        String hashed = encoder.encode(rawPassword);
        User user = new User(username, hashed, role);
        return userRepository.save(user);
    }

    public Optional<User> authenticate(String username, String rawPassword) {
        Optional<User> userOpt = userRepository.findByUsername(username);
        if (userOpt.isPresent()) {
            User user = userOpt.get();
            if (encoder.matches(rawPassword, user.getPassword())) {
                return Optional.of(user);
            }
        }
        return Optional.empty();
    }
}
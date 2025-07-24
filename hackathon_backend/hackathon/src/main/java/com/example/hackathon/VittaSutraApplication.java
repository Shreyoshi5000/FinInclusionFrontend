package com.example.hackathon;

import com.example.hackathon.model.Scenario;
import com.example.hackathon.repository.ScenarioRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.util.Arrays;

@SpringBootApplication
public class VittaSutraApplication {

	public static void main(String[] args) {
		SpringApplication.run(VittaSutraApplication.class, args);
	}


}

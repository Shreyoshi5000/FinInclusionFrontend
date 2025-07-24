package com.example.hackathon.controller;

import com.example.hackathon.model.CreditRiskForm;
import com.example.hackathon.service.CreditRiskFormService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/credit-risk")
@CrossOrigin(origins = "http://localhost:3000") // Adjust for your frontend domain
public class CreditRiskFormController {

    @Autowired
    private CreditRiskFormService service;

    @PostMapping("/save")
    public ResponseEntity<CreditRiskForm> submitForm(@RequestBody CreditRiskForm dto) {
        CreditRiskForm savedForm = service.saveForm(dto);
        return ResponseEntity.ok(savedForm);
    }

    @GetMapping("/get")
    public ResponseEntity<List<CreditRiskForm>> getAllForms() {
        List<CreditRiskForm> forms = service.getAllForms();
        return ResponseEntity.ok(forms);
    }
}

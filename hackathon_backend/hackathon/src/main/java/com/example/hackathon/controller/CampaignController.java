package com.example.hackathon.controller;

import com.example.hackathon.model.Campaign;
import com.example.hackathon.model.CampaignRegistration;
import com.example.hackathon.model.CreditRiskForm;
import com.example.hackathon.service.CampaignService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/campaigns")
@CrossOrigin(origins = "http://localhost:3000")
public class CampaignController {

    @Autowired
    private CampaignService campaignService;

    @GetMapping("/upcoming")
    public List<Campaign> getUpcomingCampaigns() {
        return campaignService.getUpcomingCampaigns();
    }

    @PostMapping("/save")
    public ResponseEntity<Campaign> submitForm(@RequestBody Campaign dto) {
        Campaign savedForm = campaignService.saveForm(dto);
        return ResponseEntity.ok(savedForm);
    }

    @PostMapping("/register")
    public CampaignRegistration registerForCampaign(@RequestBody CampaignRegistration registrationData) {
        if (registrationData.getCampaign() == null || registrationData.getCampaign().getId() == null) {
            throw new IllegalArgumentException("Campaign ID required for registration.");
        }
        if (registrationData.getUserEmail() == null || registrationData.getUserEmail().isEmpty()) {
            throw new IllegalArgumentException("User email required for registration.");
        }
        return campaignService.registerForCampaign(
                registrationData.getCampaign().getId(),
                registrationData.getUserEmail()
        );
    }
}
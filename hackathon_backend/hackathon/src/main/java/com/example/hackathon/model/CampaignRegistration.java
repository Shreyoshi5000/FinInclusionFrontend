package com.example.hackathon.model;

import jakarta.persistence.*;

@Entity
public class CampaignRegistration {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String userEmail;

    @ManyToOne
    private Campaign campaign;


    public CampaignRegistration() {}

    public CampaignRegistration(String userEmail, Campaign campaign) {
        this.userEmail = userEmail;
        this.campaign = campaign;
    }

    public Campaign getCampaign() {
        return campaign;
    }

    public void setCampaign(Campaign campaign) {
        this.campaign = campaign;
    }

    public String getUserEmail() {
        return userEmail;
    }

    public void setUserEmail(String userEmail) {
        this.userEmail = userEmail;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }
}

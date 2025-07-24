package com.example.hackathon.repository;

import com.example.hackathon.model.CampaignRegistration;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CampaignRegistrationRepository extends JpaRepository<CampaignRegistration, Long> {
}

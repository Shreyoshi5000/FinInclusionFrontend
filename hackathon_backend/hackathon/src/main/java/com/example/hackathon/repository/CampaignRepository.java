package com.example.hackathon.repository;

import com.example.hackathon.model.Campaign;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;

@Repository
public interface CampaignRepository extends JpaRepository<Campaign, Long> {
    List<Campaign> findByStartDateAfterAndRegistrationOpen(LocalDate date, boolean registrationOpen);
}
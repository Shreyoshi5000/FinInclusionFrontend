package com.example.hackathon.service;

import com.example.hackathon.model.Campaign;
import com.example.hackathon.model.CampaignRegistration;
import com.example.hackathon.model.CreditRiskForm;
import com.example.hackathon.repository.CampaignRegistrationRepository;
import com.example.hackathon.repository.CampaignRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;

@Service
public class CampaignService {

    @Autowired
    private CampaignRepository campaignRepository;

    @Autowired
    private CampaignRegistrationRepository registrationRepository;

    public List<Campaign> getUpcomingCampaigns() {
        return campaignRepository.findByStartDateAfterAndRegistrationOpen(LocalDate.now(), true);
    }

    public Campaign saveForm(Campaign dto) {
        Campaign form = new Campaign();
        form.setName(dto.getName());
        form.setDescription(dto.getDescription());
        form.setStartDate(dto.getStartDate());
        form.setEndDate(dto.getEndDate());
        form.setRegistrationOpen(dto.isRegistrationOpen());
        return campaignRepository.save(form);
    }

    public CampaignRegistration registerForCampaign(Long campaignId, String userEmail) {
        Campaign campaign = campaignRepository.findById(campaignId)
                .orElseThrow(() -> new IllegalArgumentException("Invalid Campaign ID"));
        CampaignRegistration registration = new CampaignRegistration(userEmail, campaign);
        return registrationRepository.save(registration);
    }
}

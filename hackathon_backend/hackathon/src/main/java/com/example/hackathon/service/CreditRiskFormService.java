package com.example.hackathon.service;

import com.example.hackathon.model.CreditRiskForm;
import com.example.hackathon.repository.CreditRiskFormRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CreditRiskFormService {

    @Autowired
    private CreditRiskFormRepository repository;

    public List<CreditRiskForm> getAllForms() {
        return repository.findAll();
    }

    public CreditRiskForm saveForm(CreditRiskForm dto) {
        CreditRiskForm form = new CreditRiskForm();
        form.setName(dto.getName());
        form.setAge(dto.getAge());
        form.setGender(dto.getGender());
        form.setAddress(dto.getAddress());
        form.setPhoneNumber(dto.getPhoneNumber());
        form.setNationalId(dto.getNationalId());
        form.setFamilySize(dto.getFamilySize());
        form.setOccupation(dto.getOccupation());
        form.setIncome(dto.getIncome());
        form.setBankAccount(dto.getBankAccount());
        form.setPriorLoan(dto.getPriorLoan());
        form.setLandOwnership(dto.getLandOwnership());
        return repository.save(form);
    }
}

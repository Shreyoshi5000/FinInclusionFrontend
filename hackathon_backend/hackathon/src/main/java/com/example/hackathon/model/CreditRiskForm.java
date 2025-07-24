package com.example.hackathon.model;


import jakarta.persistence.*;

@Entity
@Table(name = "credit_risk_form")
public class CreditRiskForm {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private Integer age;
    private String gender;
    private String address;
    private String phoneNumber;
    private String nationalId;
    private Integer familySize;
    private String occupation;
    private Double income;
    private Boolean bankAccount;
    private Boolean priorLoan;
    private Boolean landOwnership;

    // Getters and Setters

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public String getGender() {
        return gender;
    }

    public void setGender(String gender) {
        this.gender = gender;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    public String getNationalId() {
        return nationalId;
    }

    public void setNationalId(String nationalId) {
        this.nationalId = nationalId;
    }

    public Integer getFamilySize() {
        return familySize;
    }

    public void setFamilySize(Integer familySize) {
        this.familySize = familySize;
    }

    public String getOccupation() {
        return occupation;
    }

    public void setOccupation(String occupation) {
        this.occupation = occupation;
    }

    public Double getIncome() {
        return income;
    }

    public void setIncome(Double income) {
        this.income = income;
    }

    public Boolean getBankAccount() {
        return bankAccount;
    }

    public void setBankAccount(Boolean bankAccount) {
        this.bankAccount = bankAccount;
    }

    public Boolean getPriorLoan() {
        return priorLoan;
    }

    public void setPriorLoan(Boolean priorLoan) {
        this.priorLoan = priorLoan;
    }

    public Boolean getLandOwnership() {
        return landOwnership;
    }

    public void setLandOwnership(Boolean landOwnership) {
        this.landOwnership = landOwnership;
    }
}

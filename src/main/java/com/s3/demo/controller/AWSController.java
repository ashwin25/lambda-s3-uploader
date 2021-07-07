package com.s3.demo.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import com.s3.demo.service.AmazonService;

@Controller
public class AWSController {

    private AmazonService amazonService;

    @Autowired
    AWSController(AmazonService amazonService) {
        this.amazonService = amazonService;
    }
    
    @GetMapping("/")
    public String homepage() {
        return "index";
    }

    @PostMapping("/uploadFile")
    public String uploadFile(@RequestPart(value = "file") MultipartFile file, RedirectAttributes attributes) {
        String response = this.amazonService.uploadFile(file);
        attributes.addFlashAttribute("message", "You have successfully uploaded to the path " + response);
        return "redirect:/";
    }

    @DeleteMapping("/deleteFile")
    public String deleteFile(@RequestPart(value = "url") String fileUrl) {
        return this.amazonService.deleteFileFromS3Bucket(fileUrl);
    }
}
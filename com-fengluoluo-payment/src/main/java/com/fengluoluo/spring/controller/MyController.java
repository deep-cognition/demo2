package com.fengluoluo.spring.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class MyController {

    @GetMapping(value = "/value")
    public String mycontroller(){
        System.out.println("nihao");
        System.out.println("ddddddddddddd");
        return "myspring";
    }

}

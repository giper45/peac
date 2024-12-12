package com.example.parser;


import java.util.List;
import java.util.ArrayList;

// A simple class to demonstrate parsing
public class Filename {

    // Class variables
    private static final String CONSTANT = "constant";
    public int publicVariable;
    private String privateVariable;

    // Constructor
    public Filename() {
        this.publicVariable = 0;
        this.privateVariable = "default";
    }

    // Public method
    public void publicMethod() {
        System.out.println("Public method called");
    }

    // Private method
    private String privateMethod(String input) {
        return "Private method called with input: " + input;
    }

    // Static method
    public static void staticMethod() {
        System.out.println("Static method called");
    }

    // Method with parameters
    public int addNumbers(int a, int b) {
        return a + b;
    }

    public static void main(String[] args) {
        Filename example = new Filename();
        example.publicMethod();
        staticMethod();
        System.out.println(example.addNumbers(5, 10));
    }
}

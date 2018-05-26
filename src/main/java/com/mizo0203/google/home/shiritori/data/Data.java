package com.mizo0203.google.home.shiritori.data;

import com.fasterxml.jackson.annotation.JsonProperty;

@SuppressWarnings("unused")
public class Data {
    private final String name;
    private final String email;

    public Data(@JsonProperty("name") String name, @JsonProperty("email") String email) {
        this.name = name;
        this.email = email;
    }

    @Override
    public String toString() {
        return "Data{" + "name='" + name + '\'' + ", email='" + email + '\'' + '}';
    }
}

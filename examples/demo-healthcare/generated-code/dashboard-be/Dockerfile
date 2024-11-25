FROM openjdk:17-jdk-slim

WORKDIR /app

COPY target/dashboard-1.0.0.jar app.jar
COPY VERSION.txt /VERSION.txt

ENTRYPOINT ["java", "-jar", "app.jar"]

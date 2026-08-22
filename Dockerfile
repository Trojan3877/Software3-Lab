FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY LoanTracker.csproj ./
RUN dotnet restore LoanTracker.csproj

COPY Program.cs ./
COPY Domain/ ./Domain/
COPY Services/ ./Services/
RUN dotnet publish LoanTracker.csproj --configuration Release --no-restore --output /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/runtime:8.0
WORKDIR /app

LABEL org.opencontainers.image.source="https://github.com/CoreyLeath-code/Software3-Lab"
LABEL org.opencontainers.image.description="Software3-Lab container image"
LABEL org.opencontainers.image.licenses="MIT"

COPY --from=build /app/publish ./
USER $APP_UID
ENTRYPOINT ["dotnet", "LoanTracker.dll"]

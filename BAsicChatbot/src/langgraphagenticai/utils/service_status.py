import requests
import streamlit as st
from datetime import datetime

class ServiceStatusChecker:
    """
    Utility class to check Groq service status
    """
    
    @staticmethod
    def check_groq_status():
        """
        Check Groq service status from their status page
        """
        try:
            response = requests.get("https://groqstatus.com/api/v2/status.json", timeout=5)
            if response.status_code == 200:
                data = response.json()
                status = data.get("status", {})
                indicator = status.get("indicator", "unknown")
                description = status.get("description", "Unknown status")
                
                return {
                    "indicator": indicator,
                    "description": description,
                    "is_operational": indicator == "none"
                }
        except Exception as e:
            st.warning(f"Could not check service status: {e}")
            
        return {
            "indicator": "unknown",
            "description": "Could not determine service status",
            "is_operational": False
        }
    
    @staticmethod
    def display_service_status():
        """
        Display service status in Streamlit UI
        """
        status = ServiceStatusChecker.check_groq_status()
        
        if status["is_operational"]:
            st.success("🟢 Groq API Status: Operational")
        else:
            st.error(f"🔴 Groq API Status: {status['description']}")
            st.info("Check https://groqstatus.com/ for more details")
            
        return status

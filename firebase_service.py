# firebase_service.py
import firebase_admin
from firebase_admin import credentials, firestore, auth
import streamlit as st
from datetime import datetime
from typing import Optional, List, Dict
import os

class FirebaseService:
    _instance = None
    
    def __init__(self):
        if not firebase_admin._apps:
            # Get credentials from Streamlit secrets
            firebase_config = st.secrets.get("firebase", {})
            
            if not firebase_config:
                st.error("Firebase configuration not found in secrets. Please add it to .streamlit/secrets.toml")
                return
                
            cred_dict = {
                "type": firebase_config.get("type", ""),
                "project_id": firebase_config.get("project_id", ""),
                "private_key_id": firebase_config.get("private_key_id", ""),
                "private_key": firebase_config.get("private_key", "").replace('\\n', '\n'),
                "client_email": firebase_config.get("client_email", ""),
                "client_id": firebase_config.get("client_id", ""),
                "auth_uri": firebase_config.get("auth_uri", ""),
                "token_uri": firebase_config.get("token_uri", ""),
                "auth_provider_x509_cert_url": firebase_config.get("auth_provider_x509_cert_url", ""),
                "client_x509_cert_url": firebase_config.get("client_x509_cert_url", "")
            }
            
            try:
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
            except Exception as e:
                st.error(f"Error initializing Firebase: {e}")
                return
        
        self.db = firestore.client()
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    # User Operations
    def create_user(self, user_data: Dict) -> Optional[str]:
        """Create a new user in Firestore"""
        try:
            doc_ref = self.db.collection('users').document()
            user_data['created_at'] = datetime.now()
            doc_ref.set(user_data)
            return doc_ref.id
        except Exception as e:
            st.error(f"Error creating user: {e}")
            return None
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        try:
            doc = self.db.collection('users').document(user_id).get()
            return doc.to_dict() if doc.exists else None
        except Exception as e:
            st.error(f"Error getting user: {e}")
            return None
    
    def get_all_users(self) -> List[Dict]:
        """Get all users"""
        try:
            users = self.db.collection('users').stream()
            return [{**user.to_dict(), 'id': user.id} for user in users]
        except Exception as e:
            st.error(f"Error getting users: {e}")
            return []
    
    # Repair Request Operations
    def create_repair_request(self, request_data: Dict) -> Optional[str]:
        """Create a new repair request"""
        try:
            doc_ref = self.db.collection('repair_requests').document()
            request_data['created_at'] = datetime.now()
            request_data['status'] = 'open'
            request_data['resolved_at'] = None
            request_data['assigned_to_id'] = None
            doc_ref.set(request_data)
            return doc_ref.id
        except Exception as e:
            st.error(f"Error creating repair request: {e}")
            return None
    
    def get_repair_request(self, request_id: str) -> Optional[Dict]:
        """Get repair request by ID"""
        try:
            doc = self.db.collection('repair_requests').document(request_id).get()
            if doc.exists:
                data = doc.to_dict()
                data['id'] = doc.id
                return data
            return None
        except Exception as e:
            st.error(f"Error getting repair request: {e}")
            return None
    
    def get_all_requests(self, status: str = None) -> List[Dict]:
        """Get all repair requests, optionally filtered by status"""
        try:
            if status:
                requests = self.db.collection('repair_requests').where('status', '==', status).stream()
            else:
                requests = self.db.collection('repair_requests').stream()
            
            result = []
            for req in requests:
                data = req.to_dict()
                data['id'] = req.id
                result.append(data)
            
            # Sort by creation date (newest first)
            result.sort(key=lambda x: x.get('created_at', datetime.min), reverse=True)
            return result
        except Exception as e:
            st.error(f"Error getting repair requests: {e}")
            return []
    
    def assign_repairer(self, request_id: str, user_id: str) -> bool:
        """Assign a repairer to a request"""
        try:
            self.db.collection('repair_requests').document(request_id).update({
                'status': 'assigned',
                'assigned_to_id': user_id
            })
            return True
        except Exception as e:
            st.error(f"Error assigning repairer: {e}")
            return False
    
    def resolve_request(self, request_id: str, gratitude_note: str = "") -> bool:
        """Mark a request as resolved"""
        try:
            self.db.collection('repair_requests').document(request_id).update({
                'status': 'resolved',
                'resolved_at': datetime.now(),
                'gratitude_note': gratitude_note
            })
            return True
        except Exception as e:
            st.error(f"Error resolving request: {e}")
            return False
    
    def get_user_requests(self, user_id: str, role: str = 'requester') -> List[Dict]:
        """Get requests by user (either as requester or repairer)"""
        try:
            field = 'requester_id' if role == 'requester' else 'assigned_to_id'
            requests = self.db.collection('repair_requests').where(field, '==', user_id).stream()
            
            result = []
            for req in requests:
                data = req.to_dict()
                data['id'] = req.id
                result.append(data)
            
            return result
        except Exception as e:
            st.error(f"Error getting user requests: {e}")
            return []
    
    def get_stats(self) -> Dict:
        """Get repair statistics"""
        try:
            all_requests = self.get_all_requests()
            stats = {
                'total': len(all_requests),
                'open': 0,
                'assigned': 0,
                'resolved': 0
            }
            
            for req in all_requests:
                status = req.get('status', 'open')
                if status in stats:
                    stats[status] += 1
            
            return stats
        except Exception as e:
            st.error(f"Error getting stats: {e}")
            return {}
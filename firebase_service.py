# firebase_service.py
import streamlit as st
from datetime import datetime
from typing import Optional, List, Dict
import os

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    st.warning("Firebase not installed. Using mock data for demonstration.")

class MockFirestore:
    """Mock Firebase for testing without actual Firebase"""
    def __init__(self):
        self.users = []
        self.requests = []
        self.next_user_id = 1
        self.next_request_id = 1
    
    def create_user(self, user_data):
        user_id = f"user_{self.next_user_id}"
        user_data['id'] = user_id
        user_data['created_at'] = datetime.now()
        self.users.append(user_data)
        self.next_user_id += 1
        return user_id
    
    def get_user(self, user_id):
        return next((user for user in self.users if user['id'] == user_id), None)
    
    def get_all_users(self):
        return self.users.copy()
    
    def create_repair_request(self, request_data):
        request_id = f"req_{self.next_request_id}"
        request_data['id'] = request_id
        request_data['created_at'] = datetime.now()
        request_data['status'] = 'open'
        request_data['resolved_at'] = None
        request_data['assigned_to_id'] = None
        self.requests.append(request_data)
        self.next_request_id += 1
        return request_id
    
    def get_repair_request(self, request_id):
        return next((req for req in self.requests if req['id'] == request_id), None)
    
    def get_all_requests(self, status=None):
        if status:
            return [r for r in self.requests if r['status'] == status]
        return self.requests.copy()
    
    def assign_repairer(self, request_id, user_id):
        for req in self.requests:
            if req['id'] == request_id:
                req['status'] = 'assigned'
                req['assigned_to_id'] = user_id
                return True
        return False
    
    def resolve_request(self, request_id, gratitude_note=""):
        for req in self.requests:
            if req['id'] == request_id:
                req['status'] = 'resolved'
                req['resolved_at'] = datetime.now()
                req['gratitude_note'] = gratitude_note
                return True
        return False
    
    def get_user_requests(self, user_id, role='requester'):
        field = 'requester_id' if role == 'requester' else 'assigned_to_id'
        return [r for r in self.requests if r.get(field) == user_id]
    
    def get_stats(self):
        stats = {'total': 0, 'open': 0, 'assigned': 0, 'resolved': 0}
        for req in self.requests:
            stats['total'] += 1
            status = req.get('status', 'open')
            if status in stats:
                stats[status] += 1
        return stats

class FirebaseService:
    _instance = None
    
    def __init__(self):
        self.db = None
        self.mock_mode = False

        # Check if we should use mock mode
        use_mock = os.environ.get('USE_MOCK_DB', 'false').lower() == 'true'

        if use_mock or not FIREBASE_AVAILABLE:
            self.mock_mode = True
            self.db = MockFirestore()
            st.info("🔧 Using mock database for demonstration")
            return

        # Try to initialize Firebase
        try:
            # Check if secrets are available
            if 'firebase' not in st.secrets:
                st.warning("Firebase secrets not found in Streamlit secrets. Using mock database.")
                self.mock_mode = True
                self.db = MockFirestore()
                return

            firebase_config = st.secrets.get("firebase", {})

            if not firebase_config:
                st.warning("Firebase config empty. Using mock database.")
                self.mock_mode = True
                self.db = MockFirestore()
                return

            # Check for required fields
            required_fields = ['type', 'project_id', 'private_key', 'client_email']
            if missing_fields := [
                field
                for field in required_fields
                if field not in firebase_config or not firebase_config[field]
            ]:
                st.warning(f"Missing Firebase config fields: {missing_fields}. Using mock database.")
                self.mock_mode = True
                self.db = MockFirestore()
                return

            # Initialize Firebase only if not already initialized
            if not firebase_admin._apps:
                # Prepare credentials
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

                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)

            # Initialize Firestore
            self.db = firestore.client()
            st.success("✅ Connected to Firebase!")

        except Exception as e:
            st.error(f"⚠️ Could not connect to Firebase: {str(e)[:200]}")
            st.info("Using mock database instead.")
            self.mock_mode = True
            self.db = MockFirestore()
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    # All methods with proper error handling
    def create_user(self, user_data: Dict) -> Optional[str]:
        if self.mock_mode or not self.db:
            return self.db.create_user(user_data) if self.db else None
        
        try:
            doc_ref = self.db.collection('users').document()
            user_data['created_at'] = datetime.now()
            doc_ref.set(user_data)
            return doc_ref.id
        except Exception as e:
            st.error(f"Error creating user: {e}")
            return None
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        if self.mock_mode or not self.db:
            return self.db.get_user(user_id) if self.db else None
        
        try:
            doc = self.db.collection('users').document(user_id).get()
            return doc.to_dict() if doc.exists else None
        except Exception as e:
            st.error(f"Error getting user: {e}")
            return None
    
    def get_all_users(self) -> List[Dict]:
        if self.mock_mode or not self.db:
            return self.db.get_all_users() if self.db else []
        
        try:
            users = self.db.collection('users').stream()
            return [{**user.to_dict(), 'id': user.id} for user in users]
        except Exception as e:
            st.error(f"Error getting users: {e}")
            return []
    
    def create_repair_request(self, request_data: Dict) -> Optional[str]:
        if self.mock_mode or not self.db:
            return self.db.create_repair_request(request_data) if self.db else None

        try:
            return self._extracted_from_create_repair_request_6(request_data)
        except Exception as e:
            st.error(f"Error creating repair request: {e}")
            return None

    # TODO Rename this here and in `create_repair_request`
    def _extracted_from_create_repair_request_6(self, request_data):
        doc_ref = self.db.collection('repair_requests').document()
        request_data['created_at'] = datetime.now()
        request_data['status'] = 'open'
        request_data['resolved_at'] = None
        request_data['assigned_to_id'] = None
        doc_ref.set(request_data)
        return doc_ref.id
    
    def get_repair_request(self, request_id: str) -> Optional[Dict]:
        if self.mock_mode or not self.db:
            return self.db.get_repair_request(request_id) if self.db else None
        
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
        if self.mock_mode or not self.db:
            return self.db.get_all_requests(status) if self.db else []
        
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
        if self.mock_mode or not self.db:
            return self.db.assign_repairer(request_id, user_id) if self.db else False
        
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
        if self.mock_mode or not self.db:
            return self.db.resolve_request(request_id, gratitude_note) if self.db else False
        
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
        if self.mock_mode or not self.db:
            return self.db.get_user_requests(user_id, role) if self.db else []
        
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
        if self.mock_mode or not self.db:
            return self.db.get_stats() if self.db else {}
        
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
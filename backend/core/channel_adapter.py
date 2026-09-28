from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import datetime

class NormalizedCitizenInput(BaseModel):
    """
    Standardized citizen demand payload across all input channels.
    All multi-channel adapters convert incoming raw payloads to this common contract.
    """
    channel: str = Field(..., description="Channel name: 'web_form', 'voice_audio', 'messaging_chat', 'whatsapp_stub', 'sms_stub', 'ivr_stub'")
    raw_text: Optional[str] = Field(None, description="Raw textual input if available")
    audio_base64: Optional[str] = Field(None, description="Base64 encoded audio if submitted via voice")
    audio_format: Optional[str] = Field(None, description="Audio container e.g. 'audio/webm', 'audio/wav', 'audio/mp3'")
    sender_identifier: str = Field("anon-citizen", description="Hashed/anonymized citizen identifier (Data Minimization)")
    language_hint: Optional[str] = Field(None, description="Citizen-selected language override if provided")
    location_hint: Optional[str] = Field(None, description="Location text or coordinates if provided by channel")
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    channel_metadata: Dict[str, Any] = Field(default_factory=dict)


class ChannelAdapter(ABC):
    """
    Abstract Channel Adapter interface.
    Enables pluggable intake channels (Web, Audio, WhatsApp, SMS, IVR).
    """

    @property
    @abstractmethod
    def channel_name(self) -> str:
        pass

    @property
    @abstractmethod
    def is_live(self) -> bool:
        """Indicates whether this connector is live or a simulated/stub connector"""
        pass

    @abstractmethod
    def normalize_payload(self, raw_payload: Dict[str, Any]) -> NormalizedCitizenInput:
        """Converts incoming channel-specific request to NormalizedCitizenInput"""
        pass


class WebFormAdapter(ChannelAdapter):
    @property
    def channel_name(self) -> str:
        return "web_form"

    @property
    def is_live(self) -> bool:
        return True

    def normalize_payload(self, raw_payload: Dict[str, Any]) -> NormalizedCitizenInput:
        return NormalizedCitizenInput(
            channel="web_form",
            raw_text=raw_payload.get("text", "").strip(),
            language_hint=raw_payload.get("language_override"),
            location_hint=raw_payload.get("location_hint"),
            sender_identifier=raw_payload.get("session_id", "web-user"),
            channel_metadata={"user_agent": raw_payload.get("user_agent", "browser")}
        )


class VoiceAudioAdapter(ChannelAdapter):
    @property
    def channel_name(self) -> str:
        return "voice_audio"

    @property
    def is_live(self) -> bool:
        return True

    def normalize_payload(self, raw_payload: Dict[str, Any]) -> NormalizedCitizenInput:
        return NormalizedCitizenInput(
            channel="voice_audio",
            raw_text=raw_payload.get("transcribed_text"),
            audio_base64=raw_payload.get("audio_data"),
            audio_format=raw_payload.get("mime_type", "audio/webm"),
            language_hint=raw_payload.get("language_override"),
            location_hint=raw_payload.get("location_hint"),
            sender_identifier=raw_payload.get("session_id", "voice-user"),
            channel_metadata={"recording_duration_sec": raw_payload.get("duration", 0)}
        )


class MessagingWebhookAdapter(ChannelAdapter):
    """
    Interactive Simulated Messaging Webhook (WhatsApp / Telegram style).
    Accepts simulated webhook payload from conversational chat interface.
    """
    @property
    def channel_name(self) -> str:
        return "messaging_chat"

    @property
    def is_live(self) -> bool:
        return True

    def normalize_payload(self, raw_payload: Dict[str, Any]) -> NormalizedCitizenInput:
        msg = raw_payload.get("message", {})
        sender = raw_payload.get("sender", "simulated-mobile-user")
        return NormalizedCitizenInput(
            channel="messaging_chat",
            raw_text=msg.get("text", "").strip(),
            audio_base64=msg.get("audio_data"),
            audio_format=msg.get("mime_type"),
            language_hint=raw_payload.get("language_hint"),
            location_hint=raw_payload.get("location_hint"),
            sender_identifier=f"msg-{hash(sender) % 100000}",
            channel_metadata={"app_name": "CitizenConnect WhatsApp Simulator", "sender_masked": sender[-4:] if len(sender) >= 4 else "0000"}
        )


# ============================================================================
# STUB / MOCK ADAPTERS (Clearly labeled as non-live simulation stubs)
# ============================================================================

class WhatsAppBusinessStubAdapter(ChannelAdapter):
    @property
    def channel_name(self) -> str:
        return "whatsapp_stub"

    @property
    def is_live(self) -> bool:
        return False

    def normalize_payload(self, raw_payload: Dict[str, Any]) -> NormalizedCitizenInput:
        entry = raw_payload.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0].get("value", {})
        messages = changes.get("messages", [{}])[0]
        return NormalizedCitizenInput(
            channel="whatsapp_stub",
            raw_text=messages.get("text", {}).get("body", ""),
            sender_identifier=f"wa-{messages.get('from', 'unknown')[-4:]}",
            channel_metadata={"adapter_status": "MOCK STUB - Meta Cloud API webhook signature verified (simulated)"}
        )


class SmsGatewayStubAdapter(ChannelAdapter):
    @property
    def channel_name(self) -> str:
        return "sms_stub"

    @property
    def is_live(self) -> bool:
        return False

    def normalize_payload(self, raw_payload: Dict[str, Any]) -> NormalizedCitizenInput:
        return NormalizedCitizenInput(
            channel="sms_stub",
            raw_text=raw_payload.get("body", ""),
            sender_identifier=f"sms-{raw_payload.get('msisdn', 'unknown')[-4:]}",
            channel_metadata={"adapter_status": "MOCK STUB - GovTech National SMS Gateway (CDAC/NIC)"}
        )


class IvrVoiceStubAdapter(ChannelAdapter):
    @property
    def channel_name(self) -> str:
        return "ivr_stub"

    @property
    def is_live(self) -> bool:
        return False

    def normalize_payload(self, raw_payload: Dict[str, Any]) -> NormalizedCitizenInput:
        return NormalizedCitizenInput(
            channel="ivr_stub",
            raw_text=raw_payload.get("ivr_transcription", ""),
            sender_identifier=f"ivr-{raw_payload.get('caller_id', 'unknown')[-4:]}",
            channel_metadata={"adapter_status": "MOCK STUB - Gram Vani / Kisan Call Centre IVR Toll-Free Pipeline"}
        )


CHANNEL_REGISTRY: Dict[str, ChannelAdapter] = {
    "web_form": WebFormAdapter(),
    "voice_audio": VoiceAudioAdapter(),
    "messaging_chat": MessagingWebhookAdapter(),
    "whatsapp_stub": WhatsAppBusinessStubAdapter(),
    "sms_stub": SmsGatewayStubAdapter(),
    "ivr_stub": IvrVoiceStubAdapter()
}

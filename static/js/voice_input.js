/**
 * Feature 10: Bangla & English Voice Reporting
 * Uses Web Speech API to transcribe voice and auto-populate report fields.
 */

class VoiceReportAssistant {
    constructor(config) {
        this.btnId = config.btnId || 'voice-btn';
        this.statusId = config.statusId || 'voice-status';
        this.previewId = config.previewId || 'voice-preview';
        this.langSelectId = config.langSelectId || 'voice-lang';
        this.titleInput = document.getElementById(config.titleInputId || 'id_title');
        this.descInput = document.getElementById(config.descInputId || 'id_description');
        this.colorInput = document.getElementById(config.colorInputId || 'id_primary_color');
        this.brandInput = document.getElementById(config.brandInputId || 'id_brand');
        this.categorySelect = document.getElementById(config.categorySelectId || 'id_category');
        this.locationInput = document.getElementById(config.locationInputId || 'id_location_name');

        this.recognition = null;
        this.isRecording = false;
        this.init();
    }

    init() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            console.warn('Speech Recognition API not supported in this browser.');
            const btn = document.getElementById(this.btnId);
            if (btn) {
                btn.style.display = 'none';
            }
            return;
        }

        this.recognition = new SpeechRecognition();
        this.recognition.continuous = true;
        this.recognition.interimResults = true;

        const btn = document.getElementById(this.btnId);
        if (btn) {
            btn.addEventListener('click', () => this.toggleListening());
        }
    }

    toggleListening() {
        if (this.isRecording) {
            this.stopListening();
        } else {
            this.startListening();
        }
    }

    startListening() {
        const langElem = document.getElementById(this.langSelectId);
        this.recognition.lang = langElem ? langElem.value : 'bn-BD'; // Default Bengali (as in PDF)
        
        const btn = document.getElementById(this.btnId);
        const status = document.getElementById(this.statusId);
        const preview = document.getElementById(this.previewId);

        try {
            this.recognition.start();
            this.isRecording = true;
            if (btn) {
                btn.classList.add('bg-rose-500', 'text-white', 'animate-pulse');
                btn.classList.remove('bg-cyan-100', 'text-cyan-800');
                btn.innerHTML = '<i class="fas fa-stop mr-1.5"></i> Listening (Click to stop)';
            }
            if (status) {
                status.classList.remove('hidden');
                status.innerText = `Listening in ${this.recognition.lang === 'bn-BD' ? 'Bangla (বাংলা)' : 'English'}... Speak now!`;
            }
        } catch (e) {
            console.error(e);
        }

        this.recognition.onresult = (event) => {
            let transcript = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
                transcript += event.results[i][0].transcript;
            }

            if (preview) {
                preview.classList.remove('hidden');
                preview.innerText = `"${transcript}"`;
            }

            // Fill description and parse
            this.parseTranscriptIntoFields(transcript);
        };

        this.recognition.onerror = (event) => {
            console.warn('Speech recognition error:', event.error);
            this.stopListening();
        };

        this.recognition.onend = () => {
            this.stopListening();
        };
    }

    stopListening() {
        if (this.recognition && this.isRecording) {
            this.recognition.stop();
        }
        this.isRecording = false;
        const btn = document.getElementById(this.btnId);
        const status = document.getElementById(this.statusId);
        if (btn) {
            btn.classList.remove('bg-rose-500', 'text-white', 'animate-pulse');
            btn.classList.add('bg-cyan-100', 'text-cyan-800');
            btn.innerHTML = '<i class="fas fa-microphone mr-1.5 text-cyan-600"></i> Voice Assist (Bangla / English)';
        }
        if (status) {
            status.innerText = "Transcribed successfully! Fields updated.";
        }
    }

    parseTranscriptIntoFields(text) {
        if (!text) return;
        const lower = text.toLowerCase();

        // If description input is empty or we append
        if (this.descInput) {
            this.descInput.value = text;
        }

        // Color detection (English & Bengali transliteration)
        const colors = [
            { key: 'black', val: 'Black' }, { key: 'কালো', val: 'Black' },
            { key: 'blue', val: 'Navy Blue' }, { key: 'নীল', val: 'Blue' },
            { key: 'red', val: 'Red' }, { key: 'লাল', val: 'Red' },
            { key: 'silver', val: 'Silver' }, { key: 'সাদা', val: 'White' },
            { key: 'white', val: 'White' }, { key: 'grey', val: 'Grey' },
            { key: 'gray', val: 'Grey' }, { key: 'ধূসর', val: 'Grey' }
        ];

        for (const c of colors) {
            if (lower.includes(c.key) && this.colorInput) {
                this.colorInput.value = c.val;
                break;
            }
        }

        // Brand detection
        const brands = ['hp', 'dell', 'apple', 'macbook', 'samsung', 'lenovo', 'asus', 'acer', 'walton', 'xiaomi', 'redmi', 'oppo', 'vivo', 'casio'];
        for (const b of brands) {
            if (lower.includes(b) && this.brandInput) {
                this.brandInput.value = b.toUpperCase();
                break;
            }
        }

        // Quick Category heuristics
        if (this.categorySelect) {
            if (lower.includes('laptop') || lower.includes('ল্যাপটপ') || lower.includes('macbook') || lower.includes('কম্পিউটার')) {
                this.selectCategoryByKeyword('laptop');
            } else if (lower.includes('phone') || lower.includes('mobile') || lower.includes('ফোন') || lower.includes('মোবাইল')) {
                this.selectCategoryByKeyword('phone');
            } else if (lower.includes('bag') || lower.includes('backpack') || lower.includes('ব্যাগ')) {
                this.selectCategoryByKeyword('bag');
            } else if (lower.includes('wallet') || lower.includes('মানিব্যাগ') || lower.includes('purse')) {
                this.selectCategoryByKeyword('wallet');
            } else if (lower.includes('card') || lower.includes('কার্ড') || lower.includes('id')) {
                this.selectCategoryByKeyword('id');
            } else if (lower.includes('key') || lower.includes('চাবি')) {
                this.selectCategoryByKeyword('key');
            }
        }

        // Set Title if empty
        if (this.titleInput && (!this.titleInput.value || this.titleInput.value.length < 5)) {
            let suggestedTitle = '';
            if (this.brandInput && this.brandInput.value) {
                suggestedTitle += this.brandInput.value + ' ';
            }
            if (this.colorInput && this.colorInput.value) {
                suggestedTitle += this.colorInput.value + ' ';
            }
            suggestedTitle += 'Item';
            if (suggestedTitle !== 'Item') {
                this.titleInput.value = suggestedTitle;
            }
        }
    }

    selectCategoryByKeyword(keyword) {
        if (!this.categorySelect) return;
        for (let i = 0; i < this.categorySelect.options.length; i++) {
            const optText = this.categorySelect.options[i].text.toLowerCase();
            if (optText.includes(keyword)) {
                this.categorySelect.selectedIndex = i;
                break;
            }
        }
    }
}

window.VoiceReportAssistant = VoiceReportAssistant;

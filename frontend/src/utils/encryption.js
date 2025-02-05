import CryptoJS from 'crypto-js';

export const generateRoomKey = () => {
    return CryptoJS.lib.WordArray.random(32).toString();
};

export const encryptMessage = (message, key) => {
    return CryptoJS.AES.encrypt(message, key).toString();
};

export const decryptMessage = (encryptedMessage, key) => {
    try {
        const bytes = CryptoJS.AES.decrypt(encryptedMessage, key);
        return bytes.toString(CryptoJS.enc.Utf8);
    } catch (error) {
        console.error('Decryption failed:', error);
        return 'Message decryption failed';
    }
};

export const hashPassword = (password) => {
    return CryptoJS.SHA256(password).toString();
}; 
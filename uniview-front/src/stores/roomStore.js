import { defineStore } from 'pinia';
import axios from 'axios';
import parseJwt from '@/utils';
import Cookies from 'js-cookie';  // Можно использовать js-cookie для работы с куками
import router from '@/router';
export const useRoomStore = defineStore('room', {
    state: () => ({
        rooms: [],
    }),
    actions: {

        async createRoom(name, type, password = null) {
            try {
                
                const roomData = { name, type };
                if (type === 'private' && password) {
                    roomData.password = password;
                }

                let id_user = null;
                const token = Cookies.get('access_token');
                if(token){
                    const decoded = parseJwt(token);
                    console.log(decoded);
                    id_user = decoded.id_user;
                }

                roomData.id_user = id_user;

                console.log('Отправляем данные:', roomData);

                const response = await axios.post(
                    '/api/rooms/create_room',
                    roomData,
                    { headers: { 'Content-Type': 'application/json' } }
                );

                let room = response.data.Room;

                room.password = password;

                Cookies.set(`room_info${room.id}`, JSON.stringify(room), {expires: 1});


                router.push(`/room/${room.id}`);


                console.log(' данные:', room);

                return room; // Возвращаем объект комнаты, чтобы использовать его на фронте

            } catch (error) {
                console.error('Ошибка при создании комнаты:', error);
                throw error;
            }
        }
    },
});

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
        // async fetchRooms() {
        //   try {
        //     const response = await axios.get('http://localhost:8000/rooms');
        //     this.rooms = response.data;
        //   } catch (error) {
        //     console.error('Ошибка при загрузке комнат:', error);
        //   }
        // },
        // async createRoom(name, type, password = null) {
        //   try {
        //     const roomData = { name, type };

        //     // Если комната приватная, добавляем пароль
        //     if (type === 'private' && password) {
        //       roomData.password = password;
        //     }
        //     roomData.id_user = '172d1a6b50b84ef28e7cc813f41cf842';

        //     const response = await axios.post(
        //         'http://127.0.0.1:8000/rooms/create_room', roomData,
        //         {headers: {
        //             'Content-Type': 'application/json'
        //           },
        //           withCredentials: false,}
        //     );
        //     console.log(response);
        //     this.rooms.push(response.data.room); // Добавляем в локальный список
        //   } catch (error) {
        //     console.error('Ошибка при создании комнаты:', error);
        //   }
        // },

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
                    'http://127.0.0.1:8000/rooms/create_room',
                    roomData,
                    { headers: { 'Content-Type': 'application/json' } }
                );

                let room = response.data.Room;

                room.password = password;

                Cookies.set(`room_info${room.id}`, JSON.stringify(room), {expires: 1});

                // if(room.type === 'private' && password) {
                //     Cookies.set(`room_password${room.id}`, password, {expires: 1});
                // };

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

--Pedir datos faltantes para un proyecto de una solicitud que ya ha sido aceptada
CREATE OR REPLACE PROCEDURE guardar_proyecto_aceptado (IN vfecha_inicio DATE, IN vfecha_final DATE, IN vprioridad VARCHAR, IN vfolio_solicitud VARCHAR, INOUT pRes INTEGER) AS $$
	DECLARE
		vfecha_inicio alias for $1;
        vfecha_final alias for $2;
        vprioridad alias for $3;
        vfolio_solicitud alias for $4;

        vid_empresa integer;
        vid_solicitud integer;
        vprocentaje numeric;
        vestado varchar;
        vmonto float;

        vrec record;
        vban integer;

	BEGIN
		-- Recorrido de la tabla solicitud_proyecto para saber si existe
        Select into vrec * from solicitud_proyecto where folio_solicitud = vfolio_solicitud for update;
        -- raise notice 'vrec: %', vrec;
		--Entra si encuentra el folio de la solicitud
		IF FOUND THEN
            --Evaluar el estado de la solicitud debe estar como aceptado
            IF vrec.estado = 'aceptado' THEN
                -- Evaluar que la fecha de inicio sea mayor que la actual
                IF vfecha_inicio > current_date THEN
                    --Evalua que la fecha de inicio sea menor que ya de fin
                    IF vfecha_inicio < vfecha_final THEN
                        --Extraer los datos faltantes
                        vid_empresa := vrec.id_empresa;
                        vid_solicitud := vrec.id_empresa;
                        vmonto := vrec.monto_presupuesto;
                        vprocentaje := 0;
                        vestado := 'en proceso';
                        --inserta los datos para el proyecto aceptado
                        insert into proyecto (id_empresa, id_solicitud, fecha_inicio, fecha_fin, monto, prioridad, porcentaje_avance, estado_proyecto)
                        values (vrec.id_empresa, vid_solicitud, vfecha_inicio, vfecha_final, vmonto, vprocentaje, vprocentaje, vestado);
                        commit;
                        vban := 1; -- Mensaje exito proyecto aceptado guardado
                    ELSE
                        vban := 4; --Mensaje de error que la fecha de inicio es mayor a la final
                    END IF;
                        Pres :=vban;
                ELSE
                    vban := 2; -- Mensaje de error que la fecha de inicio es menor que la actual
                END IF;
                    pRes := vban;
            ELSE
                vban := 5; --Mensaje de error que el estado no es 'aceptado'
            END IF;
                pRes := vban;
        ELSE
            vban := 3; -- Mensaje de error solicitud no encontrada
		END IF;
			pRes := vban;
    END;
$$ LANGUAGE plpgsql;

call guardar_proyecto_aceptado ('2023-11-08', '2023-12-15', 'Alta', 'A01', NULL); -- 1
call guardar_proyecto_aceptado ('2023-11-05', '2023-12-15', 'Alta', 'A01', NULL); -- Error 2
call guardar_proyecto_aceptado ('2023-12-20', '2023-12-15', 'Alta', 'A01', NULL); -- Error 4
call guardar_proyecto_aceptado ('2023-11-08', '2023-12-15', 'Alta', 'A10', NULL); -- Error 3
call guardar_proyecto_aceptado ('2023-11-08', '2023-12-15', 'Alta', 'A02', NULL); -- Error 5

CREATE OR REPLACE PROCEDURE guardar_proyecto_aceptado (
    IN vfecha_inicio DATE,
    IN vfecha_final DATE,
    IN vprioridad VARCHAR,
    IN vfolio_solicitud VARCHAR,
    INOUT pRes INTEGER
) AS $$
DECLARE
    vid_empresa INTEGER;
    vid_solicitud INTEGER;
    vporcentaje NUMERIC;
    vestado VARCHAR;
    vmonto FLOAT;
    vrec RECORD;
    vban INTEGER;
BEGIN
    -- Recorrido de la tabla solicitud_proyecto para saber si existe
    SELECT * INTO vrec FROM solicitud_proyecto WHERE folio_solicitud = vfolio_solicitud FOR UPDATE;

    -- Entra si encuentra el folio de la solicitud
    IF FOUND THEN
        -- Evaluar el estado de la solicitud; debe estar como 'aceptado'
        IF vrec.estado = 'aceptado' THEN
            -- Evaluar que la fecha de inicio sea mayor que la actual
            IF vfecha_inicio > current_date THEN
                -- Evaluar que la fecha de inicio sea menor que la de fin
                IF vfecha_inicio < vfecha_final THEN
                    -- Extraer los datos faltantes
                    vid_empresa := vrec.id_empresa;
                    vid_solicitud := vrec.id_solicitud;
                    vmonto := vrec.monto_presupuesto;
                    vporcentaje := 0; -- Puedes ajustar esto según tus necesidades
                    vestado := 'en proceso';

                    -- Insertar los datos para el proyecto aceptado
                    INSERT INTO proyecto (
                        id_empresa,
                        id_solicitud,
                        fecha_inicio,
                        fecha_fin,
                        monto,
                        prioridad,
                        porcentaje_avance,
                        estado_proyecto
                    ) VALUES (
                        vid_empresa,
                        vid_solicitud,
                        vfecha_inicio,
                        vfecha_final,
                        vmonto,
                        vprioridad,
                        vporcentaje,
                        vestado
                    ); -- Devolver el ID del proyecto

                    vban := 1; -- Mensaje éxito: proyecto aceptado guardado
                ELSE
                    vban := 4; -- Mensaje de error: la fecha de inicio es mayor a la final
                END IF;
            ELSE
                vban := 2; -- Mensaje de error: la fecha de inicio es menor que la actual
            END IF;
        ELSE
            vban := 5; -- Mensaje de error: el estado no es 'aceptado'
        END IF;
    ELSE
        vban := 3; -- Mensaje de error: solicitud no encontrada
    END IF;

    pRes := vban;
END;
$$ LANGUAGE plpgsql;

call guardar_proyecto_aceptado ('2023-11-08', '2023-12-15', 'Alta', 'A01', NULL); -- 1
call guardar_proyecto_aceptado ('2023-11-05', '2023-12-15', 'Alta', 'A01', NULL); -- Error 2
call guardar_proyecto_aceptado ('2023-12-20', '2023-12-15', 'Alta', 'A01', NULL); -- Error 4
call guardar_proyecto_aceptado ('2023-11-08', '2023-12-15', 'Alta', 'A10', NULL); -- Error 3
call guardar_proyecto_aceptado ('2023-11-08', '2023-12-15', 'Alta', 'A02', NULL); -- Error 5

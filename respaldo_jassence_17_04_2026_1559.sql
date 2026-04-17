-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: jassencebd
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `carrito`
--

DROP TABLE IF EXISTS `carrito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carrito` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cliente_id` int DEFAULT NULL,
  `session_id` varchar(100) DEFAULT NULL,
  `creado_en` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cliente_id` (`cliente_id`),
  CONSTRAINT `carrito_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carrito`
--

LOCK TABLES `carrito` WRITE;
/*!40000 ALTER TABLE `carrito` DISABLE KEYS */;
INSERT INTO `carrito` VALUES (1,2,NULL,'2026-04-09 01:29:39'),(2,1,NULL,'2026-04-10 00:42:11');
/*!40000 ALTER TABLE `carrito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carrito_items`
--

DROP TABLE IF EXISTS `carrito_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carrito_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `carrito_id` int DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `producto_terminado_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `carrito_id` (`carrito_id`),
  KEY `producto_terminado_id` (`producto_terminado_id`),
  CONSTRAINT `carrito_items_ibfk_1` FOREIGN KEY (`carrito_id`) REFERENCES `carrito` (`id`),
  CONSTRAINT `carrito_items_ibfk_2` FOREIGN KEY (`producto_terminado_id`) REFERENCES `productos_terminados` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carrito_items`
--

LOCK TABLES `carrito_items` WRITE;
/*!40000 ALTER TABLE `carrito_items` DISABLE KEYS */;
INSERT INTO `carrito_items` VALUES (4,NULL,1,4);
/*!40000 ALTER TABLE `carrito_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id` int NOT NULL,
  `fecha_registro` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'2026-04-08 23:00:34'),(2,'2026-04-08 23:01:27'),(3,'2026-04-15 05:33:32');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `compras`
--

DROP TABLE IF EXISTS `compras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compras` (
  `id` int NOT NULL AUTO_INCREMENT,
  `proveedor_id` int DEFAULT NULL,
  `usuario_id` int DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `archivo_factura` varchar(255) DEFAULT NULL,
  `estado` varchar(50) DEFAULT NULL,
  `notas` text,
  `total` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `proveedor_id` (`proveedor_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `compras_ibfk_1` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores` (`id`),
  CONSTRAINT `compras_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compras`
--

LOCK TABLES `compras` WRITE;
/*!40000 ALTER TABLE `compras` DISABLE KEYS */;
INSERT INTO `compras` VALUES (1,2,1,'2026-04-08 23:34:31','comprobante_transferencia_07-Abr-2026_15_05_11_h.pdf','Recibido','',1791),(2,1,1,'2026-04-08 23:54:07','comprobante_transferencia_07-Abr-2026_15_05_11_h.pdf','Recibido','',3700),(3,1,1,'2026-04-09 01:31:44','comprobante_transferencia_07-Abr-2026_15_05_11_h.pdf','Recibido','',1100),(4,1,1,'2026-04-09 01:35:46','comprobante_transferencia_07-Abr-2026_15_05_11_h.pdf','Recibido','',500),(5,1,1,'2026-04-09 02:16:47','comprobante_transferencia_07-Abr-2026_15_05_11_h.pdf','Recibido','',960),(6,1,1,'2026-04-09 02:49:15','comprobante_transferencia_07-Abr-2026_15_05_11_h.pdf','Recibido','',600),(7,2,1,'2026-04-10 00:18:16','comprobante_transferencia_07-Abr-2026_15_05_11_h.pdf','cancelado','',90),(8,2,1,'2026-04-11 01:09:47','comprobante_transferencia_07-Abr-2026_15_05_11_h.pdf','Recibido','',90);
/*!40000 ALTER TABLE `compras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `corte_caja`
--

DROP TABLE IF EXISTS `corte_caja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `corte_caja` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `apertura` float DEFAULT NULL,
  `ventas_totales` float DEFAULT NULL,
  `egresos_gastos` float DEFAULT NULL,
  `utilidad_neta` float DEFAULT NULL,
  `efectivo_esperado` float DEFAULT NULL,
  `efectivo_real` float DEFAULT NULL,
  `diferencia` float DEFAULT NULL,
  `sesion_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `sesion_id` (`sesion_id`),
  CONSTRAINT `corte_caja_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `corte_caja_ibfk_2` FOREIGN KEY (`sesion_id`) REFERENCES `pos_sesion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `corte_caja`
--

LOCK TABLES `corte_caja` WRITE;
/*!40000 ALTER TABLE `corte_caja` DISABLE KEYS */;
INSERT INTO `corte_caja` VALUES (1,1,'2026-04-11',500,730,0,730,1230,1231,1,1);
/*!40000 ALTER TABLE `corte_caja` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_compras`
--

DROP TABLE IF EXISTS `detalle_compras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_compras` (
  `id` int NOT NULL AUTO_INCREMENT,
  `compra_id` int DEFAULT NULL,
  `materia_prima_id` int DEFAULT NULL,
  `presentacion_id` int DEFAULT NULL,
  `tipo_item` varchar(20) DEFAULT NULL,
  `cantidad_comprada` float DEFAULT NULL,
  `unidad_compra` varchar(50) DEFAULT NULL,
  `precio_unitario` float DEFAULT NULL,
  `multiplicador` float DEFAULT NULL,
  `subtotal` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `compra_id` (`compra_id`),
  KEY `materia_prima_id` (`materia_prima_id`),
  KEY `presentacion_id` (`presentacion_id`),
  CONSTRAINT `detalle_compras_ibfk_1` FOREIGN KEY (`compra_id`) REFERENCES `compras` (`id`),
  CONSTRAINT `detalle_compras_ibfk_2` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`),
  CONSTRAINT `detalle_compras_ibfk_3` FOREIGN KEY (`presentacion_id`) REFERENCES `presentaciones` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_compras`
--

LOCK TABLES `detalle_compras` WRITE;
/*!40000 ALTER TABLE `detalle_compras` DISABLE KEYS */;
INSERT INTO `detalle_compras` VALUES (1,1,NULL,1,'presentacion',50,'Piezas',9.82,1,491),(2,1,NULL,2,'presentacion',50,'Piezas',12,1,600),(3,1,NULL,3,'presentacion',50,'Piezas',14,1,700),(4,2,1,NULL,'materia',2,'Litros',800,1,1600),(5,2,2,NULL,'materia',2,'Litros',450,1,900),(6,2,3,NULL,'materia',2,'Litros',300,1,600),(7,2,4,NULL,'materia',4,'Litros',150,1,600),(8,3,5,NULL,'materia',2,'Litros',550,1,1100),(9,4,6,NULL,'materia',1,'Litros',500,1,500),(10,5,7,NULL,'materia',1,'Litros',460,1,460),(11,5,8,NULL,'materia',1,'Litros',500,1,500),(12,6,1,NULL,'materia',1,'Litros',600,1,600),(13,7,NULL,1,'presentacion',10,'Piezas',9,1,90),(14,8,NULL,1,'presentacion',10,'Piezas',9,1,90);
/*!40000 ALTER TABLE `detalle_compras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_recetas`
--

DROP TABLE IF EXISTS `detalle_recetas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_recetas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `receta_id` int DEFAULT NULL,
  `materia_prima_id` int DEFAULT NULL,
  `porcentaje` float DEFAULT NULL,
  `tipo_componente` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `receta_id` (`receta_id`),
  KEY `materia_prima_id` (`materia_prima_id`),
  CONSTRAINT `detalle_recetas_ibfk_1` FOREIGN KEY (`receta_id`) REFERENCES `recetas` (`id`),
  CONSTRAINT `detalle_recetas_ibfk_2` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_recetas`
--

LOCK TABLES `detalle_recetas` WRITE;
/*!40000 ALTER TABLE `detalle_recetas` DISABLE KEYS */;
INSERT INTO `detalle_recetas` VALUES (5,2,2,40,'esencia'),(6,2,4,60,'alcohol'),(7,3,1,20,'esencia'),(8,3,4,40,'alcohol'),(9,3,6,10,'fijador'),(10,3,7,20,'esencia'),(11,3,8,10,'esencia'),(16,1,1,30,'esencia'),(17,1,4,40,'alcohol'),(18,1,6,5,'fijador'),(19,1,2,15,'esencia'),(20,1,3,10,'esencia');
/*!40000 ALTER TABLE `detalle_recetas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_ventas`
--

DROP TABLE IF EXISTS `detalle_ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_ventas` (
  `venta_id` int NOT NULL,
  `producto_terminado_id` int NOT NULL,
  `cantidad` int DEFAULT NULL,
  `precio_unitario` float DEFAULT NULL,
  PRIMARY KEY (`venta_id`,`producto_terminado_id`),
  KEY `producto_terminado_id` (`producto_terminado_id`),
  CONSTRAINT `detalle_ventas_ibfk_1` FOREIGN KEY (`venta_id`) REFERENCES `ventas` (`id`),
  CONSTRAINT `detalle_ventas_ibfk_2` FOREIGN KEY (`producto_terminado_id`) REFERENCES `productos_terminados` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_ventas`
--

LOCK TABLES `detalle_ventas` WRITE;
/*!40000 ALTER TABLE `detalle_ventas` DISABLE KEYS */;
INSERT INTO `detalle_ventas` VALUES (2,4,1,180),(5,2,1,320),(6,1,1,200),(7,4,1,180),(8,5,1,350),(9,4,1,180);
/*!40000 ALTER TABLE `detalle_ventas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `direcciones_entrega`
--

DROP TABLE IF EXISTS `direcciones_entrega`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `direcciones_entrega` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cliente_id` int DEFAULT NULL,
  `nombre_receptor` varchar(100) DEFAULT NULL,
  `telefono_contacto` varchar(20) DEFAULT NULL,
  `calle_numero` varchar(200) DEFAULT NULL,
  `colonia` varchar(100) DEFAULT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `estado_provincia` varchar(100) DEFAULT NULL,
  `codigo_postal` varchar(10) DEFAULT NULL,
  `referencias` text,
  `es_principal` tinyint(1) DEFAULT NULL,
  `estado` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cliente_id` (`cliente_id`),
  CONSTRAINT `direcciones_entrega_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `direcciones_entrega`
--

LOCK TABLES `direcciones_entrega` WRITE;
/*!40000 ALTER TABLE `direcciones_entrega` DISABLE KEYS */;
INSERT INTO `direcciones_entrega` VALUES (1,1,'Juan','3224567890','Calle 9','Nuevo Mundo','Silao','Guanajuato','37800','La casa mas fea ',1,1),(2,2,'Erick','2714170990','Avenida 2','Nuevo Mundo','Silao','Guanajuato','90270','En la casa 9 gris',1,1);
/*!40000 ALTER TABLE `direcciones_entrega` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `egresos_caja`
--

DROP TABLE IF EXISTS `egresos_caja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `egresos_caja` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sesion_id` int DEFAULT NULL,
  `usuario_id` int DEFAULT NULL,
  `monto` float NOT NULL,
  `motivo` varchar(200) NOT NULL,
  `fecha` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sesion_id` (`sesion_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `egresos_caja_ibfk_1` FOREIGN KEY (`sesion_id`) REFERENCES `pos_sesion` (`id`),
  CONSTRAINT `egresos_caja_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `egresos_caja`
--

LOCK TABLES `egresos_caja` WRITE;
/*!40000 ALTER TABLE `egresos_caja` DISABLE KEYS */;
/*!40000 ALTER TABLE `egresos_caja` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log_auditoria`
--

DROP TABLE IF EXISTS `log_auditoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_auditoria` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `accion` varchar(50) DEFAULT NULL,
  `tabla_afectada` varchar(100) DEFAULT NULL,
  `registro_id` int DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `detalle` text,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `log_auditoria_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_auditoria`
--

LOCK TABLES `log_auditoria` WRITE;
/*!40000 ALTER TABLE `log_auditoria` DISABLE KEYS */;
INSERT INTO `log_auditoria` VALUES (1,1,'UPDATE','usuarios',1,'2026-04-08 17:08:59','Datos de jassencemail@gmail.com actualizados correctamente'),(2,1,'UPDATE','usuarios',1,'2026-04-08 17:09:18','Datos de jassencemail@gmail.com actualizados correctamente'),(3,NULL,'CREATE','Recetas',1,'2026-04-09 00:05:18','Nueva fórmula creada: Red Velvet N.0'),(4,1,'LOGOUT','accesos',1,'2026-04-08 18:06:11','Cierre de sesión manual'),(5,NULL,'LOGIN_FALLIDO','accesos',1,'2026-04-08 18:44:57','Intento Fallido: Contraseña incorrecta para jassencemail@gmail.com'),(6,1,'LOGIN','accesos',1,'2026-04-08 18:48:31','Inicio de sesión exitoso'),(7,NULL,'CREATE','Recetas',2,'2026-04-09 01:16:38','Nueva fórmula creada: Mamba Negra'),(8,1,'UPDATE','ordenes_produccion',1,'2026-04-08 19:24:55','Estado: pendiente -> en_proceso'),(9,1,'UPDATE','ordenes_produccion',1,'2026-04-08 19:25:04','Estado: en_proceso -> terminado'),(10,1,'LOGOUT','accesos',1,'2026-04-08 20:36:52','Cierre de sesión manual'),(11,1,'LOGIN','accesos',1,'2026-04-08 20:44:28','Inicio de sesión exitoso'),(12,1,'LOGOUT','accesos',1,'2026-04-08 20:49:19','Cierre de sesión manual'),(13,1,'LOGIN','accesos',1,'2026-04-08 20:53:21','Inicio de sesión exitoso'),(14,1,'UPDATE','ordenes_produccion',2,'2026-04-08 20:58:18','Estado: pendiente -> en_proceso'),(15,1,'UPDATE','ordenes_produccion',2,'2026-04-08 20:58:25','Estado: en_proceso -> terminado'),(16,NULL,'CREATE','Recetas',3,'2026-04-09 03:00:26','Nueva fórmula creada: Stars No.17'),(17,1,'LOGIN','accesos',1,'2026-04-09 13:54:23','Inicio de sesión exitoso'),(18,1,'LOGIN','accesos',1,'2026-04-09 17:43:17','Inicio de sesión exitoso'),(19,NULL,'DELETE_LOGICO','Recetas',3,'2026-04-09 23:43:53','Fórmula inhabilitada (Baja Lógica): Stars No.17 (ID: 3)'),(20,1,'DELETE','usuarios',2,'2026-04-09 17:58:00','Baja a el usuario erick.contacto0109@gmail.com'),(21,1,'CREATE','usuarios',2,'2026-04-09 17:58:14','Se ha reactivado el usuario erick.contacto0109@gmail.com'),(22,1,'DELETE','usuarios',2,'2026-04-09 18:32:06','Baja a el usuario erick.contacto0109@gmail.com'),(23,1,'CREATE','usuarios',2,'2026-04-09 18:32:13','Se ha reactivado el usuario erick.contacto0109@gmail.com'),(24,1,'DELETE','usuarios',2,'2026-04-09 18:33:57','Baja a el usuario erick.contacto0109@gmail.com'),(25,1,'CREATE','usuarios',2,'2026-04-09 18:34:03','Se ha reactivado el usuario erick.contacto0109@gmail.com'),(26,NULL,'UPDATE','ordenes_produccion',3,'2026-04-09 18:43:52','Estado: pendiente -> en_proceso'),(27,NULL,'UPDATE','ordenes_produccion',3,'2026-04-09 18:43:58','Estado: en_proceso -> terminado'),(28,1,'LOGOUT','accesos',1,'2026-04-09 19:55:14','Cierre de sesión manual'),(29,1,'LOGIN','accesos',1,'2026-04-09 19:58:31','Inicio de sesión exitoso'),(30,1,'UPDATE','ordenes_produccion',4,'2026-04-09 20:02:39','Estado: pendiente -> en_proceso'),(31,1,'UPDATE','ordenes_produccion',4,'2026-04-09 20:02:46','Estado: en_proceso -> terminado'),(32,NULL,'UPDATE','ordenes_produccion',5,'2026-04-09 20:13:41','Estado: pendiente -> en_proceso'),(33,NULL,'UPDATE','ordenes_produccion',5,'2026-04-09 20:13:48','Estado: en_proceso -> terminado'),(34,1,'UPDATE','ordenes_produccion',6,'2026-04-10 18:37:46','Estado: pendiente -> en_proceso'),(35,1,'UPDATE','ordenes_produccion',6,'2026-04-10 18:37:55','Estado: en_proceso -> terminado'),(36,1,'SALIDA','materias_primas',6,'2026-04-10 18:37:56','Consumo por Orden #6 (2x Mamba Negra): [ 0.80 de Ambar, 1.20 de Etanol ]'),(37,1,'ENTRADA','productos_terminados',5,'2026-04-10 18:37:56','Entrada a stock por Orden #6: +2 de Mamba Negra Mediana 50ml'),(38,1,'SALIDA','productos_terminados',8,'2026-04-10 18:56:30','Venta mostrador #8: [ 1x Mamba Negra Mediana 50ml ]'),(39,1,'ENTRADA','materias_primas',8,'2026-04-10 19:14:30','Entrada por compra #8: [ 10.0 de Producto Desconocido ]'),(40,1,'MERMA','merma_inventario',4,'2026-04-10 19:28:44','Merma registrada: 1 unidades en etapa Almacén'),(41,1,'MERMA','merma_inventario(MP)',1,'2026-04-10 19:42:51','Merma registrada: 60.0 Mililitros de Esencia Vainilla'),(42,1,'MERMA','merma_inventario',3,'2026-04-10 19:44:42','Merma en Almacén: -1 Red Velvet N.0 Mediana 50ml. Razón: Ruptura'),(43,1,'MERMA','merma_inventario(PRODUCTO)',4,'2026-04-10 19:46:06','Merma en Almacén: -1 Mamba Negra Mediana 50ml. Razón: Ruptura'),(44,1,'UPDATE','recetas',1,'2026-04-11 07:50:04','Modificaciones: Agregó MP 6 (0.0%) | Precio (Pres. 3): $450.0 -> $440.0'),(45,1,'UPDATE','recetas',1,'2026-04-11 07:51:44','Modificaciones: Agregó MP 6 (5.0%) | Modificó % MP 2: 20.0% -> 15.0%'),(46,1,'UPDATE','recetas',3,'2026-04-11 07:52:22','Fórmula reactivada: Stars No.17 (ID: 3)'),(47,1,'DELETE','recetas',2,'2026-04-11 07:54:35','Fórmula inhabilitada (Baja Lógica): Mamba Negra (ID: 2)'),(48,1,'UPDATE','recetas',2,'2026-04-11 07:58:37','Fórmula reactivada: Mamba Negra (ID: 2)'),(49,1,'DELETE','recetas',2,'2026-04-11 08:37:47','Fórmula inhabilitada (Baja Lógica): Mamba Negra (ID: 2)'),(50,1,'UPDATE','recetas',2,'2026-04-11 08:38:02','Fórmula reactivada: Mamba Negra (ID: 2)'),(51,1,'DELETE','recetas',2,'2026-04-11 08:42:08','Fórmula inhabilitada (Baja Lógica): Mamba Negra (ID: 2)'),(52,1,'UPDATE','recetas',2,'2026-04-11 08:42:34','Fórmula reactivada: Mamba Negra (ID: 2)'),(53,1,'DELETE','recetas',2,'2026-04-11 08:49:44','Fórmula inhabilitada (Baja Lógica): Mamba Negra (ID: 2)'),(54,1,'UPDATE','recetas',2,'2026-04-11 08:50:18','Fórmula reactivada: Mamba Negra (ID: 2)'),(55,1,'UPDATE','ordenes_produccion',7,'2026-04-14 20:25:29','Estado: pendiente -> en_proceso'),(56,1,'UPDATE','ordenes_produccion',7,'2026-04-14 20:25:54','Estado: en_proceso -> terminado'),(57,1,'SALIDA','materias_primas',7,'2026-04-14 20:25:55','Consumo por Orden #7 (1x Mamba Negra): [ 0.40 de Ambar, 0.60 de Etanol ]'),(58,1,'UPDATE','ordenes_produccion',8,'2026-04-14 20:31:58','Estado: pendiente -> en_proceso'),(59,1,'UPDATE','ordenes_produccion',8,'2026-04-14 20:32:07','Estado: en_proceso -> terminado'),(60,1,'SALIDA','materias_primas',8,'2026-04-14 20:32:08','Consumo por Orden #8 (10x Red Velvet N.0): [ 3.00 de Esencia Vainilla, 4.00 de Etanol, 0.50 de Fijador , 1.50 de Ambar, 1.00 de Azafran ]'),(61,1,'ENTRADA','productos_terminados',2,'2026-04-14 20:32:08','Entrada a stock por Orden #8: +10 de Red Velvet N.0 Mediana 50ml'),(62,1,'RESPALDOS','accesos',1,'2026-04-14 23:32:24','Accedio a respaldos'),(63,3,'UPDATE','usuarios',3,'2026-04-14 23:36:28','Datos de carlos_kbzuky@hotmail.com actualizados correctamente'),(64,3,'LOGOUT','accesos',3,'2026-04-14 23:38:17','Cierre de sesión manual'),(65,1,'RESPALDOS','accesos',1,'2026-04-14 23:38:28','Accedio a respaldos'),(66,1,'RESPALDOS','accesos',1,'2026-04-17 15:59:31','Accedio a respaldos'),(67,1,'RESPALDOS','accesos',1,'2026-04-17 15:59:42','Accedio a respaldos');
/*!40000 ALTER TABLE `log_auditoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materias_primas`
--

DROP TABLE IF EXISTS `materias_primas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materias_primas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `cantidad_disponible` float DEFAULT NULL,
  `stock_apartado` float DEFAULT '0',
  `unidad_medida` varchar(50) DEFAULT NULL,
  `stock_minimo` float DEFAULT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materias_primas`
--

LOCK TABLES `materias_primas` WRITE;
/*!40000 ALTER TABLE `materias_primas` DISABLE KEYS */;
INSERT INTO `materias_primas` VALUES (1,'Esencia Vainilla',2751,0,'Mililitros',2000,'esencia'),(2,'Ambar',1823,0,'Mililitros',2000,'esencia'),(3,'Azafran',1937,0,'Mililitros',2000,'esencia'),(4,'Etanol',3634,0,'Mililitros',4000,'alcohol'),(5,'Esencia Manzana Verde',2000,0,'Mililitros',2000,'esencia'),(6,'Fijador ',975,0,'Mililitros',1000,'fijador'),(7,'Esencia Frutal',1000,0,'Mililitros',1000,'esencia'),(8,'Esencia Lavanda',1000,0,'Mililitros',1000,'esencia');
/*!40000 ALTER TABLE `materias_primas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `merma_inventario`
--

DROP TABLE IF EXISTS `merma_inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `merma_inventario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo_item` varchar(50) DEFAULT NULL,
  `item_id` int DEFAULT NULL,
  `etapa` varchar(50) DEFAULT NULL,
  `usuario_id` int DEFAULT NULL,
  `cantidad_perdida` float DEFAULT NULL,
  `unidad_medida` varchar(50) DEFAULT NULL,
  `motivo` varchar(100) DEFAULT NULL,
  `descripcion` text,
  `orden_produccion_id` int DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `orden_produccion_id` (`orden_produccion_id`),
  CONSTRAINT `merma_inventario_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `merma_inventario_ibfk_2` FOREIGN KEY (`orden_produccion_id`) REFERENCES `ordenes_produccion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `merma_inventario`
--

LOCK TABLES `merma_inventario` WRITE;
/*!40000 ALTER TABLE `merma_inventario` DISABLE KEYS */;
INSERT INTO `merma_inventario` VALUES (1,'producto_terminado',4,'Almacén',NULL,1,'unidad','Ruptura','Se me cayo',1,'2026-04-11 01:28:44'),(2,'materia_prima',1,'Recepción',NULL,60,'Mililitros','Derrame','Accidente',NULL,'2026-04-11 01:42:51'),(3,'producto_terminado',2,'Almacén',NULL,1,'unidad','Ruptura','Se cayo',2,'2026-04-11 01:44:42'),(4,'producto_terminado',5,'Almacén',NULL,1,'unidad','Ruptura','Lo tiró el de almacen',6,'2026-04-11 01:46:06');
/*!40000 ALTER TABLE `merma_inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metodos_pago_cliente`
--

DROP TABLE IF EXISTS `metodos_pago_cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metodos_pago_cliente` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cliente_id` int NOT NULL,
  `stripe_customer_id` varchar(50) NOT NULL,
  `stripe_payment_method_id` varchar(50) NOT NULL,
  `tipo_tarjeta` varchar(20) DEFAULT NULL,
  `ultimos_4` varchar(4) DEFAULT NULL,
  `exp_mes` int DEFAULT NULL,
  `exp_anio` int DEFAULT NULL,
  `estado` tinyint(1) DEFAULT NULL,
  `es_principal` tinyint(1) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cliente_id` (`cliente_id`),
  CONSTRAINT `metodos_pago_cliente_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metodos_pago_cliente`
--

LOCK TABLES `metodos_pago_cliente` WRITE;
/*!40000 ALTER TABLE `metodos_pago_cliente` DISABLE KEYS */;
/*!40000 ALTER TABLE `metodos_pago_cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordenes_produccion`
--

DROP TABLE IF EXISTS `ordenes_produccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordenes_produccion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `receta_id` int DEFAULT NULL,
  `venta_id` int DEFAULT NULL,
  `producto_terminado_id` int DEFAULT NULL,
  `cantidad_producir` int DEFAULT NULL,
  `responsable_id` int DEFAULT NULL,
  `fecha_solicitud` datetime DEFAULT NULL,
  `fecha_inicio` datetime DEFAULT NULL,
  `fecha_fin` datetime DEFAULT NULL,
  `estado` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `receta_id` (`receta_id`),
  KEY `venta_id` (`venta_id`),
  KEY `producto_terminado_id` (`producto_terminado_id`),
  KEY `responsable_id` (`responsable_id`),
  CONSTRAINT `ordenes_produccion_ibfk_1` FOREIGN KEY (`receta_id`) REFERENCES `recetas` (`id`),
  CONSTRAINT `ordenes_produccion_ibfk_2` FOREIGN KEY (`venta_id`) REFERENCES `ventas` (`id`),
  CONSTRAINT `ordenes_produccion_ibfk_3` FOREIGN KEY (`producto_terminado_id`) REFERENCES `productos_terminados` (`id`),
  CONSTRAINT `ordenes_produccion_ibfk_4` FOREIGN KEY (`responsable_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordenes_produccion`
--

LOCK TABLES `ordenes_produccion` WRITE;
/*!40000 ALTER TABLE `ordenes_produccion` DISABLE KEYS */;
INSERT INTO `ordenes_produccion` VALUES (1,2,NULL,4,1,1,'2026-04-08 19:24:16','2026-04-08 19:24:55','2026-04-08 19:25:04','terminado'),(2,1,NULL,2,1,1,'2026-04-08 20:58:12','2026-04-08 20:58:18','2026-04-08 20:58:25','terminado'),(3,1,5,2,1,NULL,'2026-04-10 00:43:08','2026-04-09 18:43:52','2026-04-09 18:43:58','terminado'),(4,1,NULL,1,1,1,'2026-04-09 20:02:31','2026-04-09 20:02:39','2026-04-09 20:02:46','terminado'),(5,2,7,4,1,NULL,'2026-04-10 02:13:12','2026-04-09 20:13:41','2026-04-09 20:13:48','terminado'),(6,2,NULL,5,2,1,'2026-04-10 18:37:39','2026-04-10 18:37:46','2026-04-10 18:37:55','terminado'),(7,2,9,4,1,1,'2026-04-14 20:24:29','2026-04-14 20:25:29','2026-04-14 20:25:54','terminado'),(8,1,NULL,2,10,1,'2026-04-14 20:31:39','2026-04-14 20:31:58','2026-04-14 20:32:07','terminado');
/*!40000 ALTER TABLE `ordenes_produccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pos_items`
--

DROP TABLE IF EXISTS `pos_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pos_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sesion_id` int DEFAULT NULL,
  `producto_terminado_id` int DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sesion_id` (`sesion_id`),
  CONSTRAINT `pos_items_ibfk_1` FOREIGN KEY (`sesion_id`) REFERENCES `pos_sesion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pos_items`
--

LOCK TABLES `pos_items` WRITE;
/*!40000 ALTER TABLE `pos_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `pos_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pos_sesion`
--

DROP TABLE IF EXISTS `pos_sesion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pos_sesion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `abierta_en` datetime DEFAULT NULL,
  `estado` varchar(50) DEFAULT NULL,
  `monto_apertura` float DEFAULT NULL,
  `cerrada_en` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pos_sesion`
--

LOCK TABLES `pos_sesion` WRITE;
/*!40000 ALTER TABLE `pos_sesion` DISABLE KEYS */;
INSERT INTO `pos_sesion` VALUES (1,1,'2026-04-09 02:54:53','cerrada',500,'2026-04-11 14:30:28'),(2,1,'2026-04-16 01:03:19','cerrada',100,'2026-04-16 01:18:09'),(3,1,'2026-04-16 01:18:23','abierta',100,NULL);
/*!40000 ALTER TABLE `pos_sesion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `presentaciones`
--

DROP TABLE IF EXISTS `presentaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `presentaciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `mililitros` int DEFAULT NULL,
  `stock_botes` int DEFAULT NULL,
  `stock_botes_apartado` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `presentaciones`
--

LOCK TABLES `presentaciones` WRITE;
/*!40000 ALTER TABLE `presentaciones` DISABLE KEYS */;
INSERT INTO `presentaciones` VALUES (1,'Chica',30,53,0),(2,'Mediana',50,26,0),(3,'Grande',100,48,0);
/*!40000 ALTER TABLE `presentaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produccion_temporal`
--

DROP TABLE IF EXISTS `produccion_temporal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produccion_temporal` (
  `id` int NOT NULL AUTO_INCREMENT,
  `receta_id` int DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `creado_por` int DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `presentacion_id` int DEFAULT NULL,
  `estatus` varchar(20) DEFAULT NULL,
  `venta_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `presentacion_id` (`presentacion_id`),
  KEY `fk_produccion_venta` (`venta_id`),
  CONSTRAINT `fk_produccion_venta` FOREIGN KEY (`venta_id`) REFERENCES `ventas` (`id`),
  CONSTRAINT `produccion_temporal_ibfk_1` FOREIGN KEY (`presentacion_id`) REFERENCES `presentaciones` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produccion_temporal`
--

LOCK TABLES `produccion_temporal` WRITE;
/*!40000 ALTER TABLE `produccion_temporal` DISABLE KEYS */;
INSERT INTO `produccion_temporal` VALUES (12,7,100,1,'2026-04-15 00:00:00',3,'pendiente',NULL);
/*!40000 ALTER TABLE `produccion_temporal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos_terminados`
--

DROP TABLE IF EXISTS `productos_terminados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos_terminados` (
  `id` int NOT NULL AUTO_INCREMENT,
  `receta_id` int DEFAULT NULL,
  `presentacion_id` int DEFAULT NULL,
  `stock_disponible_venta` int DEFAULT NULL,
  `stock_minimo` int DEFAULT NULL,
  `precio_venta` float DEFAULT NULL,
  `estado` varchar(50) DEFAULT NULL,
  `stock_comprometido` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_producto` (`receta_id`,`presentacion_id`),
  KEY `presentacion_id` (`presentacion_id`),
  CONSTRAINT `productos_terminados_ibfk_1` FOREIGN KEY (`receta_id`) REFERENCES `recetas` (`id`),
  CONSTRAINT `productos_terminados_ibfk_2` FOREIGN KEY (`presentacion_id`) REFERENCES `presentaciones` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos_terminados`
--

LOCK TABLES `productos_terminados` WRITE;
/*!40000 ALTER TABLE `productos_terminados` DISABLE KEYS */;
INSERT INTO `productos_terminados` VALUES (1,1,1,0,5,200,'activo',0),(2,1,2,11,5,320,'activo',0),(3,1,3,0,5,440,'activo',0),(4,2,1,0,5,180,'Activo',0),(5,2,2,0,5,350,'Activo',0),(6,2,3,0,5,570,'Activo',0),(7,3,1,0,5,170,'Activo',0),(8,3,2,0,5,250,'Activo',0),(9,3,3,0,5,380,'Activo',0),(10,4,1,0,5,100,'activo',0),(11,4,2,0,5,150,'activo',0),(12,4,3,0,5,230,'activo',0),(13,5,1,0,5,120,'activo',0),(14,5,2,0,5,210,'activo',0),(15,5,3,0,5,350,'activo',0),(16,6,1,0,5,120,'activo',0),(17,6,2,0,5,210,'activo',0),(18,6,3,0,5,350,'activo',0),(19,7,1,0,5,60,'activo',0),(20,7,2,8,5,100,'activo',0),(21,7,3,0,5,380,'activo',0);
/*!40000 ALTER TABLE `productos_terminados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedores`
--

DROP TABLE IF EXISTS `proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_empresa` varchar(150) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` text,
  `tipo_insumos` varchar(100) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores`
--

LOCK TABLES `proveedores` WRITE;
/*!40000 ALTER TABLE `proveedores` DISABLE KEYS */;
INSERT INTO `proveedores` VALUES (1,'Esencias y Materiales Lozmar','(81) 2189 5026','José Santos Chocano #2503\r\nCol. Martínez C.P. 64550\r\nMonterrey, Nuevo León','Químicos',1),(2,'Nihao Jewelry','(861) 9517936749','Hangzhou, China','Empaques',1);
/*!40000 ALTER TABLE `proveedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recetas`
--

DROP TABLE IF EXISTS `recetas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recetas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_perfume` varchar(150) DEFAULT NULL,
  `inspiracion` varchar(150) DEFAULT NULL,
  `descripcion` text,
  `imagen_url` varchar(255) DEFAULT NULL,
  `genero` varchar(50) DEFAULT NULL,
  `ocasion` varchar(50) DEFAULT NULL,
  `familia_olfativa` varchar(50) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recetas`
--

LOCK TABLES `recetas` WRITE;
/*!40000 ALTER TABLE `recetas` DISABLE KEYS */;
INSERT INTO `recetas` VALUES (1,'Red Velvet No.4','MFK Baccarat','Sensación dulce','image_1775693058819.jpg','Femenino','Formal','Dulce',1),(2,'Mamba Negra','Black Death','Noche olfativa','image_1775697365051.jpg','Masculino','Noche','Sandalo',1),(3,'Stars No.17','Dior Homme','Floral','image_1775699249801.jpg','Femenino','Noche','Dulce',1),(4,'Addicted No.3','YSL Black','Jasmin, Naranja','image_1776298263850.jpg','Femenino','Casual','Floral',1),(5,'Do. Zafrica No.110','Bal D\' Afrique','Fresca','image_1776298589277.jpg','Unisex','Casual','Citrica',1),(6,'Ocean Breeze','Acqua di Gio',' Frescura de mar con limón y madera suave.','image_1776300049899.jpg','Masculino','Diario','Citrica Acuatica',1),(7,'Vainilla & Tabaco','Inspirado en \"Tom Ford Tobacco Vainilla\"','Aroma profundo a Vainilla y tabaco','image_1776300049899.jpg','Masculino','Formal','Amaderada',1);
/*!40000 ALTER TABLE `recetas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(80) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'cliente','Cliente estándar del e-commerce'),(2,'admin','Administrador general del sistema Jassence'),(3,'ventas','Personal encargado de gestionar pedidos y clientes'),(4,'produccion','Personal encargado de manufactura, recetas y mermas'),(5,'inventario','Personal encargado de materias primas y proveedores');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles_users`
--

DROP TABLE IF EXISTS `roles_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles_users` (
  `usuario_id` int DEFAULT NULL,
  `rol_id` int DEFAULT NULL,
  KEY `usuario_id` (`usuario_id`),
  KEY `rol_id` (`rol_id`),
  CONSTRAINT `roles_users_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `roles_users_ibfk_2` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles_users`
--

LOCK TABLES `roles_users` WRITE;
/*!40000 ALTER TABLE `roles_users` DISABLE KEYS */;
INSERT INTO `roles_users` VALUES (1,2),(2,3),(3,4),(4,5),(5,1);
/*!40000 ALTER TABLE `roles_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `fs_uniquifier` varchar(255) NOT NULL,
  `tf_primary_method` varchar(64) DEFAULT NULL,
  `tf_totp_secret` varchar(255) DEFAULT NULL,
  `tf_phone_number` varchar(128) DEFAULT NULL,
  `nombre` varchar(150) DEFAULT NULL,
  `apellidos` varchar(150) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `fs_uniquifier` (`fs_uniquifier`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'jassencemail@gmail.com','$2b$12$rrj93CcYtrkKSg0BZa2B1uAkBY140CujmtIGpOp3zxPcHPpf06ZQa',1,'988b01f80b7d4b9e8634829c1b8df2c7','email','{\"enckey\":{\"c\":14,\"k\":\"XE5HOY5C42VL73GNBOZMJJHXE2S34VAJ\",\"s\":\"FDSTYZ7MLVF6TXI3MPWA\",\"t\":\"1\",\"v\":1},\"type\":\"totp\",\"v\":1}',NULL,'Dueño','Jassence',''),(2,'erick.contacto0109@gmail.com','$2b$12$XxFGtEjWe2JSmWsSITMiUOw1UxYiz4xjCEPI/.RzRfvBqsQQsMRu2',1,'cf5b819d13344867a966cb24ee46efda','email','{\"enckey\":{\"c\":14,\"k\":\"MIJZXYNPNDDIC57BVWP44FBXFDDUG3EK\",\"s\":\"NCW5KGUD2BNKXVN2G6TA\",\"t\":\"1\",\"v\":1},\"type\":\"totp\",\"v\":1}',NULL,'Erick','Blanco','2714170990'),(3,'carlos_kbzuky@hotmail.com','$2b$12$0hrH6KSDcBoSFO7XeGARFOsAwXzDXDrz9DcPvc4OLAdY0Fr9yTyum',1,'a3de0220103045b08f2f9b0da4adc2f8','email','{\"enckey\":{\"c\":14,\"k\":\"5DDC5PDG7AIUY4O27QV7K4IENPABKT2C\",\"s\":\"W5LCVJMUSIZGNTEZKMVA\",\"t\":\"1\",\"v\":1},\"type\":\"totp\",\"v\":1}',NULL,'Carlos','Gutierrez',''),(4,'lolala2@outlook.es','$2b$12$9FUeT08yLCnT9VhuIC4yjuPxITKmaCKbFGNCo/amIBmtLihgj93sW',0,'a4aba104e82b4ba2b2a3376d712b2482',NULL,NULL,NULL,'Rafa','Martinez',''),(5,'srk0white@gmail.com','$2b$12$dB0JoNYe5AarQQLAESHOZO/3pS0nLRsTN4Ef6xcZU0.p5OShl2SJ.',1,'992f5f667a6e46039ed5fa6f5b2de553','email','{\"enckey\":{\"c\":14,\"k\":\"LBEDUYC347XDACEQ5OH6MRJ6BNZ3YAGL\",\"s\":\"JMEQCQAIEFSGZDORTJJQ\",\"t\":\"1\",\"v\":1},\"type\":\"totp\",\"v\":1}',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `cliente_id` int DEFAULT NULL,
  `direccion_envio_id` int DEFAULT NULL,
  `pasarela_online` varchar(30) DEFAULT NULL,
  `metodo_pago_id` int DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `canal_venta` varchar(50) DEFAULT NULL,
  `estado_pedido` varchar(50) DEFAULT NULL,
  `total_venta` float DEFAULT NULL,
  `metodo_pago_fisico` varchar(50) DEFAULT NULL,
  `sesion_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `cliente_id` (`cliente_id`),
  KEY `direccion_envio_id` (`direccion_envio_id`),
  KEY `metodo_pago_id` (`metodo_pago_id`),
  KEY `sesion_id` (`sesion_id`),
  CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`),
  CONSTRAINT `ventas_ibfk_3` FOREIGN KEY (`direccion_envio_id`) REFERENCES `direcciones_entrega` (`id`),
  CONSTRAINT `ventas_ibfk_4` FOREIGN KEY (`metodo_pago_id`) REFERENCES `metodos_pago_cliente` (`id`),
  CONSTRAINT `ventas_ibfk_5` FOREIGN KEY (`sesion_id`) REFERENCES `pos_sesion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (2,1,NULL,NULL,NULL,NULL,'2026-04-09 02:55:24','Mostrador','Entregado',180,'efectivo',1),(5,NULL,1,1,'PayPal',NULL,'2026-04-10 00:43:08','Online','Enviado',371.2,NULL,NULL),(6,1,NULL,NULL,NULL,NULL,'2026-04-10 02:11:35','Mostrador','Entregado',200,'efectivo',1),(7,NULL,2,2,'PayPal',NULL,'2026-04-10 02:13:12','Online','Enviado',208.8,NULL,NULL),(8,1,NULL,NULL,NULL,NULL,'2026-04-11 00:56:30','Mostrador','Entregado',350,'efectivo',1),(9,NULL,2,2,'PayPal',NULL,'2026-04-15 02:23:16','Online','Enviado',208.8,NULL,NULL),(10,NULL,2,2,'PayPal',NULL,'2026-04-15 07:32:17','Online','Enviado',232,NULL,NULL),(11,NULL,2,2,'PayPal',NULL,'2026-04-15 21:09:51','Online','Enviado',429.2,NULL,NULL),(12,NULL,5,3,'PayPal',NULL,'2026-04-16 01:01:22','Online','Enviado',533.6,NULL,NULL),(13,1,NULL,NULL,NULL,NULL,'2026-04-16 01:15:39','Mostrador','Entregado',200,'tarjeta',2);
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'jassencebd'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-17 15:59:44

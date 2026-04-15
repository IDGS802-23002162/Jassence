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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carrito`
--

LOCK TABLES `carrito` WRITE;
/*!40000 ALTER TABLE `carrito` DISABLE KEYS */;
INSERT INTO `carrito` VALUES (5,3,NULL,'2026-04-08 08:22:42'),(6,NULL,'307c52ef-e90e-4bca-a0a8-e9d960fa1d0c','2026-04-09 20:45:18'),(7,1,NULL,'2026-04-13 19:34:16');
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
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carrito_items`
--

LOCK TABLES `carrito_items` WRITE;
/*!40000 ALTER TABLE `carrito_items` DISABLE KEYS */;
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
INSERT INTO `clientes` VALUES (1,'2026-04-08 05:27:30'),(3,'2026-04-08 08:22:21');
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compras`
--

LOCK TABLES `compras` WRITE;
/*!40000 ALTER TABLE `compras` DISABLE KEYS */;
INSERT INTO `compras` VALUES (1,1,1,'2026-04-08 06:03:37','comprobanteFAKE.png','Recibido','',510),(2,1,1,'2026-04-08 06:09:22','comprobanteFAKE.png','Recibido','',170),(3,1,1,'2026-04-08 06:42:56','comprobanteFAKE.png','Recibido','',1500),(4,1,1,'2026-04-08 06:44:21','comprobanteFAKE.png','Recibido','',975),(5,1,1,'2026-04-13 20:16:52','comprobante_transferencia_09-Abr-2026_15_22_56_h.pdf','Recibido','',150),(6,1,1,'2026-04-13 21:13:43','comprobante_transferencia_09-Abr-2026_15_22_56_h.pdf','Recibido','',300);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `corte_caja`
--

LOCK TABLES `corte_caja` WRITE;
/*!40000 ALTER TABLE `corte_caja` DISABLE KEYS */;
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
  `compra_id` int NOT NULL,
  `materia_prima_id` int DEFAULT NULL,
  `presentacion_id` int DEFAULT NULL,
  `tipo_item` varchar(20) DEFAULT 'materia',
  `cantidad_comprada` float DEFAULT NULL,
  `unidad_compra` varchar(50) DEFAULT NULL,
  `precio_unitario` float DEFAULT NULL,
  `multiplicador` float DEFAULT '1',
  `subtotal` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_detalle_compra` (`compra_id`),
  KEY `fk_detalle_materia` (`materia_prima_id`),
  KEY `fk_detalle_presentacion` (`presentacion_id`),
  CONSTRAINT `fk_detalle_compra` FOREIGN KEY (`compra_id`) REFERENCES `compras` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_detalle_materia` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`),
  CONSTRAINT `fk_detalle_presentacion` FOREIGN KEY (`presentacion_id`) REFERENCES `presentaciones` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_compras`
--

LOCK TABLES `detalle_compras` WRITE;
/*!40000 ALTER TABLE `detalle_compras` DISABLE KEYS */;
INSERT INTO `detalle_compras` VALUES (1,3,NULL,1,'presentacion',100,'Piezas',15,1,1500),(2,4,5,NULL,'materia',1,'Litros',125,1,125),(3,4,NULL,2,'presentacion',50,'Piezas',17,1,850),(4,5,NULL,3,'presentacion',10,'Piezas',15,1,150),(5,6,6,NULL,'materia',1,'Litros',130,1,130),(6,6,7,NULL,'materia',2,'Litros',85,1,170);
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_recetas`
--

LOCK TABLES `detalle_recetas` WRITE;
/*!40000 ALTER TABLE `detalle_recetas` DISABLE KEYS */;
INSERT INTO `detalle_recetas` VALUES (4,2,1,40,'esencia'),(5,2,4,50,'alcohol'),(6,2,3,10,'fijador'),(7,3,1,40,'esencia'),(8,3,4,50,'alcohol'),(9,3,3,5,'fijador'),(10,3,5,5,'esencia');
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
INSERT INTO `detalle_ventas` VALUES (2,1,1,100),(4,1,1,100),(5,2,1,150),(6,3,1,280),(7,2,2,150),(8,1,1,100),(8,5,1,230),(9,2,1,150),(10,5,5,230),(11,2,1,150);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `direcciones_entrega`
--

LOCK TABLES `direcciones_entrega` WRITE;
/*!40000 ALTER TABLE `direcciones_entrega` DISABLE KEYS */;
INSERT INTO `direcciones_entrega` VALUES (1,3,'Erick','2714170990','Avenida 1','Nuevo Mundo','Silao','Guanajuato','36112','Casa fea',1,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_auditoria`
--

LOCK TABLES `log_auditoria` WRITE;
/*!40000 ALTER TABLE `log_auditoria` DISABLE KEYS */;
INSERT INTO `log_auditoria` VALUES (1,1,'UPDATE','usuarios',1,'2026-04-07 23:31:26','Datos de erick.contacto0109@gmail.com actualizados correctamente'),(2,NULL,'CREATE','Recetas',2,'2026-04-08 06:16:47','Nueva fórmula creada: LeParfum MAX'),(3,1,'UPDATE','ordenes_produccion',1,'2026-04-08 01:41:11','Estado: pendiente -> en_proceso'),(4,1,'UPDATE','ordenes_produccion',1,'2026-04-08 01:41:25','Estado: en_proceso -> terminado'),(5,1,'CREATE','usuarios',2,'2026-04-08 02:09:00','Se ha reistrado lolala2@outlook.es correctamente'),(6,2,'LOGIN','accesos',2,'2026-04-08 02:10:09','Inicio de sesión exitoso'),(7,2,'LOGOUT','accesos',2,'2026-04-08 02:21:20','Cierre de sesión manual'),(8,1,'LOGOUT','accesos',1,'2026-04-08 02:25:24','Cierre de sesión manual'),(9,1,'LOGIN','accesos',1,'2026-04-09 13:43:16','Inicio de sesión exitoso'),(10,NULL,'LOGIN_FALLIDO','accesos',1,'2026-04-09 14:37:34','Intento Fallido: Contraseña incorrecta para erick.contacto0109@gmail.com'),(11,NULL,'LOGIN_FALLIDO','accesos',1,'2026-04-09 14:37:44','Intento Fallido: Contraseña incorrecta para erick.contacto0109@gmail.com'),(12,1,'LOGIN','accesos',1,'2026-04-09 14:38:10','Inicio de sesión exitoso'),(13,1,'UPDATE','recetas',2,'2026-04-13 02:43:37','Fórmula reactivada: LeParfum MAX (ID: 2)'),(14,1,'DELETE','recetas',2,'2026-04-13 02:43:38','Fórmula inhabilitada (Baja Lógica): LeParfum MAX (ID: 2)'),(15,1,'UPDATE','recetas',2,'2026-04-13 02:43:47','Fórmula reactivada: LeParfum MAX (ID: 2)'),(16,1,'UPDATE','ordenes_produccion',2,'2026-04-13 02:44:15','Estado: pendiente -> en_proceso'),(17,1,'UPDATE','ordenes_produccion',3,'2026-04-13 02:44:16','Estado: pendiente -> en_proceso'),(18,1,'UPDATE','ordenes_produccion',2,'2026-04-13 02:44:19','Estado: en_proceso -> terminado'),(19,1,'SALIDA','materias_primas',2,'2026-04-13 02:44:20','Consumo por Orden #2 (10x LeParfum MAX): [ 4.00 de Esencia Amaderada, 5.00 de Alcohol Nuevo, 1.00 de Fijador 3000 ]'),(20,1,'ENTRADA','productos_terminados',2,'2026-04-13 02:44:20','Entrada a stock por Orden #2: +10 de LeParfum MAX Mediana 50ml'),(21,1,'UPDATE','ordenes_produccion',3,'2026-04-13 02:44:21','Estado: en_proceso -> terminado'),(22,1,'SALIDA','materias_primas',3,'2026-04-13 02:44:21','Consumo por Orden #3 (10x LeParfum MAX): [ 4.00 de Esencia Amaderada, 5.00 de Alcohol Nuevo, 1.00 de Fijador 3000 ]'),(23,1,'ENTRADA','productos_terminados',1,'2026-04-13 02:44:21','Entrada a stock por Orden #3: +10 de LeParfum MAX Chica 30ml'),(24,1,'DELETE','recetas',2,'2026-04-13 02:44:35','Fórmula inhabilitada (Baja Lógica): LeParfum MAX (ID: 2)'),(25,1,'UPDATE','recetas',2,'2026-04-13 02:44:47','Fórmula reactivada: LeParfum MAX (ID: 2)'),(26,1,'UPDATE','ordenes_produccion',4,'2026-04-13 13:59:04','Estado: pendiente -> en_proceso'),(27,1,'UPDATE','ordenes_produccion',4,'2026-04-13 13:59:06','Estado: en_proceso -> terminado'),(28,1,'SALIDA','materias_primas',4,'2026-04-13 13:59:07','Consumo por Orden #4 (1x LeParfum MAX): [ 0.40 de Esencia Amaderada, 0.50 de Alcohol Nuevo, 0.10 de Fijador 3000 ]'),(29,1,'ENTRADA','productos_terminados',1,'2026-04-13 13:59:07','Entrada a stock por Orden #4: +1 de LeParfum MAX Chica 30ml'),(30,1,'UPDATE','ordenes_produccion',5,'2026-04-13 14:07:16','Estado: pendiente -> en_proceso'),(31,1,'UPDATE','ordenes_produccion',5,'2026-04-13 14:07:19','Estado: en_proceso -> terminado'),(32,1,'SALIDA','materias_primas',5,'2026-04-13 14:07:19','Consumo por Orden #5 (1x LeParfum MAX): [ 0.40 de Esencia Amaderada, 0.50 de Alcohol Nuevo, 0.10 de Fijador 3000 ]'),(33,1,'ENTRADA','materias_primas',5,'2026-04-13 14:16:54','Entrada por compra #5: [ 10.0 de Producto Desconocido ]'),(34,1,'UPDATE','ordenes_produccion',6,'2026-04-13 14:17:14','Estado: pendiente -> en_proceso'),(35,1,'UPDATE','ordenes_produccion',6,'2026-04-13 14:17:26','Estado: en_proceso -> terminado'),(36,1,'SALIDA','materias_primas',6,'2026-04-13 14:17:27','Consumo por Orden #6 (1x LeParfum MAX): [ 0.40 de Esencia Amaderada, 0.50 de Alcohol Nuevo, 0.10 de Fijador 3000 ]'),(37,1,'UPDATE','ordenes_produccion',7,'2026-04-13 14:19:07','Estado: pendiente -> en_proceso'),(38,1,'UPDATE','ordenes_produccion',7,'2026-04-13 14:19:15','Estado: en_proceso -> terminado'),(39,1,'SALIDA','materias_primas',7,'2026-04-13 14:19:16','Consumo por Orden #7 (2x LeParfum MAX): [ 0.80 de Esencia Amaderada, 1.00 de Alcohol Nuevo, 0.20 de Fijador 3000 ]'),(40,1,'CREATE','recetas',3,'2026-04-13 14:22:32','Nueva fórmula creada: Mi Nueva Elegancia'),(41,1,'UPDATE','ordenes_produccion',8,'2026-04-13 14:26:58','Estado: pendiente -> en_proceso'),(42,1,'UPDATE','ordenes_produccion',9,'2026-04-13 14:27:00','Estado: pendiente -> en_proceso'),(43,1,'UPDATE','ordenes_produccion',8,'2026-04-13 14:28:34','Estado: en_proceso -> terminado'),(44,1,'SALIDA','materias_primas',8,'2026-04-13 14:28:35','Consumo por Orden #8 (1x LeParfum MAX): [ 0.40 de Esencia Amaderada, 0.50 de Alcohol Nuevo, 0.10 de Fijador 3000 ]'),(45,1,'UPDATE','ordenes_produccion',9,'2026-04-13 14:28:36','Estado: en_proceso -> terminado'),(46,1,'SALIDA','materias_primas',9,'2026-04-13 14:28:37','Consumo por Orden #9 (1x Mi Nueva Elegancia): [ 0.40 de Esencia Amaderada, 0.50 de Alcohol Nuevo, 0.05 de Fijador 3000, 0.05 de Esencia de Vainilla ]'),(47,1,'ENTRADA','materias_primas',6,'2026-04-13 15:13:46','Entrada por compra #6: [ 1.0 de Etanol, 2.0 de Fijador New ]'),(48,1,'UPDATE','ordenes_produccion',10,'2026-04-13 18:48:24','Estado: pendiente -> en_proceso'),(49,1,'UPDATE','ordenes_produccion',10,'2026-04-13 18:49:01','Estado: en_proceso -> terminado'),(50,1,'SALIDA','materias_primas',10,'2026-04-13 18:49:01','Consumo por Orden #10 (10x Mi Nueva Elegancia): [ 4.00 de Esencia Amaderada, 5.00 de Alcohol Nuevo, 0.50 de Fijador 3000, 0.50 de Esencia de Vainilla ]'),(51,1,'ENTRADA','productos_terminados',5,'2026-04-13 18:49:01','Entrada a stock por Orden #10: +10 de Mi Nueva Elegancia Mediana 50ml'),(52,1,'UPDATE','ordenes_produccion',11,'2026-04-13 18:49:37','Estado: pendiente -> en_proceso'),(53,1,'UPDATE','ordenes_produccion',11,'2026-04-13 18:49:58','Estado: en_proceso -> terminado'),(54,1,'SALIDA','materias_primas',11,'2026-04-13 18:49:58','Consumo por Orden #11 (1x LeParfum MAX): [ 0.40 de Esencia Amaderada, 0.50 de Alcohol Nuevo, 0.10 de Fijador 3000 ]'),(55,1,'UPDATE','ordenes_produccion',12,'2026-04-13 18:53:42','Estado: pendiente -> en_proceso'),(56,1,'UPDATE','ordenes_produccion',12,'2026-04-13 18:54:03','Estado: en_proceso -> terminado'),(57,1,'SALIDA','materias_primas',12,'2026-04-13 18:54:03','Consumo por Orden #12 (1x LeParfum MAX): [ 0.40 de Esencia Amaderada, 0.50 de Alcohol Nuevo, 0.10 de Fijador 3000 ]'),(58,1,'ENTRADA','productos_terminados',3,'2026-04-13 18:54:03','Entrada a stock por Orden #12: +1 de LeParfum MAX Grande 100ml'),(59,1,'UPDATE','ordenes_produccion',13,'2026-04-13 18:59:46','Estado: pendiente -> en_proceso'),(60,1,'UPDATE','ordenes_produccion',13,'2026-04-13 19:00:04','Estado: en_proceso -> terminado'),(61,1,'SALIDA','materias_primas',13,'2026-04-13 19:00:04','Consumo por Orden #13 (5x Mi Nueva Elegancia): [ 2.00 de Esencia Amaderada, 2.50 de Alcohol Nuevo, 0.25 de Fijador 3000, 0.25 de Esencia de Vainilla ]');
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
  `unidad_medida` varchar(50) DEFAULT NULL,
  `stock_minimo` float DEFAULT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `stock_apartado` float DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materias_primas`
--

LOCK TABLES `materias_primas` WRITE;
/*!40000 ALTER TABLE `materias_primas` DISABLE KEYS */;
INSERT INTO `materias_primas` VALUES (1,'Esencia Amaderada',164,'Mililitros',1000,'esencia',0),(2,'Etanol Potente',2000,'Mililitros',1500,'etanol',0),(3,'Fijador 3000',1831,'Mililitros',1000,'fijador',0),(4,'Alcohol Nuevo',955,'Mililitros',1000,'alcohol',0),(5,'Esencia de Vainilla',960,'Mililitros',1000,'esencia',0),(6,'Etanol',1000,'Mililitros',2000,'alcohol',0),(7,'Fijador New',2000,'Mililitros',1000,'fijador',0);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `merma_inventario`
--

LOCK TABLES `merma_inventario` WRITE;
/*!40000 ALTER TABLE `merma_inventario` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordenes_produccion`
--

LOCK TABLES `ordenes_produccion` WRITE;
/*!40000 ALTER TABLE `ordenes_produccion` DISABLE KEYS */;
INSERT INTO `ordenes_produccion` VALUES (1,2,NULL,1,1,1,'2026-04-08 01:37:21','2026-04-08 01:41:11','2026-04-08 01:41:25','terminado'),(2,2,NULL,2,10,1,'2026-04-08 01:37:45','2026-04-13 02:44:15','2026-04-13 02:44:19','terminado'),(3,2,NULL,1,10,1,'2026-04-13 02:44:12','2026-04-13 02:44:16','2026-04-13 02:44:21','terminado'),(4,2,NULL,1,1,1,'2026-04-13 13:58:32','2026-04-13 13:59:04','2026-04-13 13:59:06','terminado'),(5,2,5,2,1,1,'2026-04-13 14:07:09','2026-04-13 14:07:16','2026-04-13 14:07:19','terminado'),(6,2,6,3,1,1,'2026-04-13 14:17:08','2026-04-13 14:17:14','2026-04-13 14:17:26','terminado'),(7,2,7,2,2,1,'2026-04-13 14:18:58','2026-04-13 14:19:07','2026-04-13 14:19:15','terminado'),(8,2,8,1,1,1,'2026-04-13 14:26:53','2026-04-13 14:26:58','2026-04-13 14:28:34','terminado'),(9,3,8,5,1,1,'2026-04-13 14:26:56','2026-04-13 14:27:00','2026-04-13 14:28:36','terminado'),(10,3,NULL,5,10,1,'2026-04-13 18:48:18','2026-04-13 18:48:24','2026-04-13 18:49:01','terminado'),(11,2,9,2,1,1,'2026-04-13 18:49:26','2026-04-13 18:49:37','2026-04-13 18:49:58','terminado'),(12,2,NULL,3,1,1,'2026-04-13 18:53:32','2026-04-13 18:53:42','2026-04-13 18:54:03','terminado'),(13,3,10,5,5,1,'2026-04-13 18:59:13','2026-04-13 18:59:46','2026-04-13 19:00:04','terminado');
/*!40000 ALTER TABLE `ordenes_produccion` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `tr_actualizar_estado_venta_nuevo` AFTER INSERT ON `ordenes_produccion` FOR EACH ROW BEGIN
    IF NEW.venta_id IS NOT NULL AND NEW.estado = 'pendiente' THEN
        UPDATE ventas 
        SET estado_pedido = 'Esperando Producción'
        WHERE id = NEW.venta_id AND canal_venta = 'Online';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_update_orden` AFTER UPDATE ON `ordenes_produccion` FOR EACH ROW INSERT INTO log_auditoria (
    usuario_id,
    accion,
    tabla_afectada,
    registro_id,
    fecha,
    detalle
)
VALUES (
    NEW.responsable_id,
    'UPDATE',
    'ordenes_produccion',
    NEW.id,
    NOW(),
    CONCAT('Estado: ', OLD.estado, ' -> ', NEW.estado)
) */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `tr_actualizar_estado_venta_produccion` AFTER UPDATE ON `ordenes_produccion` FOR EACH ROW BEGIN
    IF NEW.venta_id IS NOT NULL THEN
        IF NEW.estado = 'pendiente' THEN
            UPDATE ventas 
            SET estado_pedido = 'Esperando Producción'
            WHERE id = NEW.venta_id AND canal_venta = 'Online';
        ELSEIF NEW.estado = 'en_proceso' THEN
            UPDATE ventas 
            SET estado_pedido = 'En Producción'
            WHERE id = NEW.venta_id AND canal_venta = 'Online';
        ELSEIF NEW.estado = 'terminado' THEN
            UPDATE ventas 
            SET estado_pedido = 'Listo para enviar'
            WHERE id = NEW.venta_id AND canal_venta = 'Online';
        END IF;
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pos_sesion`
--

LOCK TABLES `pos_sesion` WRITE;
/*!40000 ALTER TABLE `pos_sesion` DISABLE KEYS */;
INSERT INTO `pos_sesion` VALUES (1,2,'2026-04-08 08:10:45','abierta',500,NULL),(2,1,'2026-04-13 08:43:14','abierta',100,NULL);
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
  `stock_botes` int DEFAULT '0',
  `stock_botes_apartado` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `presentaciones`
--

LOCK TABLES `presentaciones` WRITE;
/*!40000 ALTER TABLE `presentaciones` DISABLE KEYS */;
INSERT INTO `presentaciones` VALUES (1,'Chica',30,87,0),(2,'Mediana',50,20,0),(3,'Grande',100,8,0);
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
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produccion_temporal`
--

LOCK TABLES `produccion_temporal` WRITE;
/*!40000 ALTER TABLE `produccion_temporal` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos_terminados`
--

LOCK TABLES `productos_terminados` WRITE;
/*!40000 ALTER TABLE `productos_terminados` DISABLE KEYS */;
INSERT INTO `productos_terminados` VALUES (1,2,1,11,5,100,'Activo',1),(2,2,2,13,5,150,'Activo',1),(3,2,3,2,5,280,'Activo',0),(4,3,1,0,5,130,'activo',0),(5,3,2,10,5,230,'activo',6),(6,3,3,0,5,360,'activo',0);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores`
--

LOCK TABLES `proveedores` WRITE;
/*!40000 ALTER TABLE `proveedores` DISABLE KEYS */;
INSERT INTO `proveedores` VALUES (1,'QuimiKa SA de CV','4716789023','No aplica','Químicos',1);
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
  `activo` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recetas`
--

LOCK TABLES `recetas` WRITE;
/*!40000 ALTER TABLE `recetas` DISABLE KEYS */;
INSERT INTO `recetas` VALUES (2,'LeParfum MAX','Dolce','Amaderado dulce','81orRSLdl0L._AC_UY218_.jpg','Masculino','Casual','Amaderado',1),(3,'Mi Nueva Elegancia','Hugo Boss','Olfativo','image_1776111720876.jpg','Masculino','Formal','Amaderado',1);
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
INSERT INTO `roles_users` VALUES (1,2),(2,3),(3,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'erick.contacto0109@gmail.com','$2b$12$drNKRCzgfD3qZx34t0Nd0uwuSzvix4Sy93/KYhWyrVXFoVd/efv2a',1,'80d26009b1904dbea44ac13213461044','email','{\"enckey\":{\"c\":14,\"k\":\"7UXD2OT66NE6PEVNX46II3F62B2G7SYK\",\"s\":\"CZREYSJJYU4APIEUKJFA\",\"t\":\"1\",\"v\":1},\"type\":\"totp\",\"v\":1}',NULL,'Erick','Blanco','2714170990'),(2,'lolala2@outlook.es','$2b$12$rWm3mYE9uZmdLGStHVkrT.b8wucfJjPQj05mp.1Q4VJ5YH./IpA4i',1,'18bcff3c2bd643a3b26c569154e424e1','email','{\"enckey\":{\"c\":14,\"k\":\"C3CF5VDPG55UHVNFCYAO66BL7BPG2RZI\",\"s\":\"VQKSEZGMHFDWRTOZLNVQ\",\"t\":\"1\",\"v\":1},\"type\":\"totp\",\"v\":1}',NULL,'Pancho','Juarez','3228901234'),(3,'kcirecraftxd@gmail.com','$2b$12$M5oj/DlwTPbnTXgwHqSN5exi.2gGKB3Ta7n73pVZUDnfqL1Riaws6',1,'da5fea7fce15478b93f637d9f7ceac6b','email','{\"enckey\":{\"c\":14,\"k\":\"62QQ72XHJ2D22LQQTPI2AL7JTC6LVG5M\",\"s\":\"SRZC4RPI7UP4HWC3BNQQ\",\"t\":\"1\",\"v\":1},\"type\":\"totp\",\"v\":1}',NULL,NULL,NULL,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (2,2,NULL,NULL,NULL,NULL,'2026-04-08 08:11:04','Mostrador','Entregado',100,'efectivo',1),(4,NULL,3,1,'PayPal',NULL,'2026-04-13 19:36:06','Online','Pagado - En Producción (Envío rápido)',116,NULL,NULL),(5,NULL,3,1,'PayPal',NULL,'2026-04-13 19:59:43','Online','Pagado - En Producción (Envío rápido)',174,NULL,NULL),(6,NULL,3,1,'PayPal',NULL,'2026-04-13 20:16:07','Online','Enviado',324.8,NULL,NULL),(7,NULL,3,1,'PayPal',NULL,'2026-04-13 20:18:41','Online','Enviado',348,NULL,NULL),(8,NULL,3,1,'PayPal',NULL,'2026-04-13 20:23:12','Online','Enviado',382.8,NULL,NULL),(9,NULL,3,1,'PayPal',NULL,'2026-04-14 00:49:21','Online','Listo para enviar',174,NULL,NULL),(10,NULL,3,1,'PayPal',NULL,'2026-04-14 00:58:59','Online','Listo para enviar',1334,NULL,NULL),(11,NULL,3,1,'PayPal',NULL,'2026-04-14 01:02:30','Online','Cancelado',174,NULL,NULL);
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

-- Dump completed on 2026-04-14 17:38:40
